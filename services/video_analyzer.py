import base64
import re
import uuid
import cv2
import numpy as np
from .openpose_service import OpenPoseService
from .stroke_recognition_manager import StrokeRecognitionManager

class VideoAnalyzer:
    MAX_QUEUE_SIZE = 4
    ALLOWED_MIME_TYPES = [
        'video/mp4'
    ]
    LEFT_LEG_JOINT = 11
    RIGHT_LEG_JOINT = 14
    COURT_SPACE_DIMENSIONS = (100, 100)

    def __init__(self, openpose_service: OpenPoseService, encoded_video: str, court_coordinates: list):
        self.openpose_service = openpose_service
        self.encoded_video = encoded_video
        self.top_player_stroke_recognition_manager = StrokeRecognitionManager()
        self.bottom_player_stroke_recognition_manager = StrokeRecognitionManager()
        self.court_transformation_matrix = self.__get_court_space_transformation_matrix(court_coordinates)

    def analyze_video(self):
        video_capture = self.__load_video_capture_from_base64(self.encoded_video)

        result = []

        success, frame = video_capture.read()

        while success:
            poses = self.openpose_service.get_players_from_frame(frame)

            top_pose = poses.get('top')
            bottom_pose = poses.get('bottom')

            stroke_top_player = self.top_player_stroke_recognition_manager.handle_stroke(top_pose)
            stroke_bottom_player = self.top_player_stroke_recognition_manager.handle_stroke(bottom_pose)

            position_top_player = self.__get_player_position(top_pose)
            position_bottom_player = self.__get_player_position(bottom_pose)

            result.append({
                'top_player': {
                    'position': position_top_player,
                    'stroke': stroke_top_player,
                    'pose': top_pose,
                },
                'bottom_player': {
                    'position': position_bottom_player,
                    'stroke': stroke_bottom_player,
                    'pose': bottom_pose,
                }
            })

            success, image = video_capture.read()

        video_capture.release()
        return result

    def __load_video_capture_from_base64(self, encoded_video) -> cv2.VideoCapture:
        mime_type = self.__get_mime_type(encoded_video)
        if mime_type not in self.ALLOWED_MIME_TYPES:
            raise Exception('Uploaded video does not have correct type')

        sanitized_encoded_data = encoded_video.split(',')[1]
        extension = mime_type.split('/')[1]
        tmp_file_name = f'./{uuid.uuid4()}.{extension}'

        tmp_file = open(tmp_file_name, 'wb')
        tmp_file.write(base64.b64decode(sanitized_encoded_data))
        tmp_file.close()

        return cv2.VideoCapture(tmp_file_name)

    def __get_player_position(self, pose):
        left_leg = pose[self.LEFT_LEG_JOINT]
        right_leg = pose[self.RIGHT_LEG_JOINT]

        if left_leg == (0, 0) or right_leg == (0, 0):
            return None

        center_point = ((left_leg[0] + right_leg[0]) / 2, (left_leg[1] + right_leg[1]) / 2)
        return self.__warp_point_to_court_space(center_point)

    def __get_mime_type(self, encoded_data):
        data_without_prefix = re.sub(r'^data:', '', encoded_data)
        return data_without_prefix.split(';')[0]

    def __get_court_space_transformation_matrix(self, court_coordinates):
        court_space_corners = []
        for height_offset in [0, 1]:
            for width_offset in [0, 1]:
                court_space_corners.append((
                    self.COURT_SPACE_DIMENSIONS[0] * width_offset,
                    self.COURT_SPACE_DIMENSIONS[1] * height_offset,
                ))

        return cv2.getPerspectiveTransform(np.float32(court_coordinates), np.float32(court_space_corners))

    def __warp_point_to_court_space(self, point):
        d = self.court_transformation_matrix[2, 0] * point[0] + self.court_transformation_matrix[2, 1] * point[1] + self.court_transformation_matrix[2, 2]

        return (
            int((self.court_transformation_matrix[0, 0] * point[0] + self.court_transformation_matrix[0, 1] * point[1] + self.court_transformation_matrix[0, 2]) / d),
            int((self.court_transformation_matrix[1, 0] * point[0] + self.court_transformation_matrix[1, 1] * point[1] + self.court_transformation_matrix[1, 2]) / d),
        )


