import tensorflow_hub as hub
import tensorflow as tf
from .pose_extraction_service import PoseExtractionService
from badminton_cv_utils.utils.keypoints_loader import get_bottom_person, get_top_person

class MovenetPoseExtractionService(PoseExtractionService):
    def __init__(self):
        model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
        self.movenet = model.signatures['serving_default']

    def get_players_from_frame(self, frame):
        img = frame.copy()
        img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 384, 640)
        input_img = tf.cast(img, dtype=tf.int32)

        results = self.movenet(input_img)
        keypoints_with_scores = results['output_0'].numpy()[:, :, :51].reshape((6, 17, 3))
        keypoints = self.__get_people_keypoints(frame, keypoints_with_scores)

        _, width, _ = frame.shape
        bottom_player = get_bottom_person(width, keypoints)
        top_player = get_top_person(width, keypoints, bottom_player)

        return {
            'top': self.__transform_to_relative(frame, top_player),
            'bottom': self.__transform_to_relative(frame, bottom_player),
        }

    def __transform_to_relative(self, frame, pose):
        if pose is None:
            return None

        y, x, _ = frame.shape
        return [[point[0] / x, point[1] / y] for point in pose]

    def __get_people_keypoints(self, frame, network_output):
        y, x, _ = frame.shape
        people = []
        for person in network_output:
          person = self.__normalize_pose(person)
          person = [[int(point[1] * x), int(point[0] * y)] for point in person]
          people.append(person)
        return people

    def __normalize_pose(self, pose):
        top_neck = self.__get_middle(pose[5], pose[6])
        bottom_body = self.__get_middle(pose[11], pose[12])

        return [
            self.__get_point(pose[0]),
            top_neck,

            self.__get_point(pose[6]),
            self.__get_point(pose[8]),
            self.__get_point(pose[10]),

            self.__get_point(pose[5]),
            self.__get_point(pose[7]),
            self.__get_point(pose[9]),

            bottom_body,

            self.__get_point(pose[12]),
            self.__get_point(pose[14]),
            self.__get_point(pose[16]),

            self.__get_point(pose[11]),
            self.__get_point(pose[13]),
            self.__get_point(pose[15]),
        ]

    def __get_middle(self, point1, point2):
      x = ((point2[0] - point1[0]) / 2) + point1[0]
      y = ((point2[1] - point1[1]) / 2) + point1[1]
      return [x, y]

    def __get_point(self, point):
      x, y, _ = point
      return [x, y]