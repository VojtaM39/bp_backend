from .pose_extraction_service import PoseExtractionService

class MockPoseExtractionService(PoseExtractionService):
    SEQUENCE_LENGTH = 11
    X_OFFSET_RATIO = 0.01
    TOP_Y_OFFSET = 0.4
    BOTTOM_Y_OFFSET = 0.8
    BASE_POSE = [
        [0.5, 0.0],
        [0.5, 0.05],

        [0.45, 0.05],
        [0.45, 0.07],
        [0.45, 0.09],

        [0.55, 0.05],
        [0.55, 0.07],
        [0.55, 0.09],

        [0.5, 0.1],

        [0.45, 0.12],
        [0.45, 0.15],
        [0.45, 0.19],

        [0.55, 0.12],
        [0.55, 0.15],
        [0.55, 0.19],
    ]

    def __init__(self):
        self.idx = 0

    def get_players_from_frame(self, frame):
        x_offset = (self.idx % MockPoseExtractionService.SEQUENCE_LENGTH) - (MockPoseExtractionService.SEQUENCE_LENGTH // 2 + 1)
        x_offset *= MockPoseExtractionService.X_OFFSET_RATIO

        self.idx += 1

        top_pose = [[point[0] - x_offset, point[1] + MockPoseExtractionService.TOP_Y_OFFSET] for point in MockPoseExtractionService.BASE_POSE]
        bottom_pose = [[point[0] - x_offset, point[1] + MockPoseExtractionService.BOTTOM_Y_OFFSET] for point in MockPoseExtractionService.BASE_POSE]

        return {
            'top': top_pose,
            'bottom': bottom_pose
        }
