# from openpose import pyopenpose as op
from .pose_extraction_service import PoseExtractionService
# from badminton_cv_utils.utils.keypoints_loader import get_bottom_person, get_top_person
# FIXME

class OpenposePoseExtractionService(PoseExtractionService):
    MODEL_PATH = '~/openpose/models'
    #
    # def __init__(self):
    #     params = dict()
    #     params["model_folder"] = OpenposePoseExtractionService.MODEL_PATH
    #
    #     self.opWrapper = op.WrapperPython()
    #     self.opWrapper.configure(params)
    #     self.opWrapper.start()
    #
    # def get_players_from_frame(self, frame):
    #     datum = op.Datum()
    #     datum.cvInputData = frame
    #
    #     self.opWrapper.emplaceAndPop(op.VectorDatum([datum]))
    #     network_output = datum.poseKeypoints
    #     keypoints = self.__get_people_keypoints(network_output)
    #
    #     _, width, _ = frame.shape
    #     bottom_player = get_bottom_person(width, keypoints)
    #     top_player = get_top_person(width, keypoints, bottom_player)
    #
    #     return {
    #         'top': bottom_player,
    #         'bottom': top_player
    #     }
    #
    # def __get_people_keypoints(self, network_output):
    #     keypoints = []
    #     for human in network_output:
    #         pose = []
    #         for i in range(len(human)):
    #             pose.append((int(human[i][0]), int(human[i][1])))
    #         keypoints.append(pose)
    #     return keypoints
