from .pose_extraction_service import PoseExtractionService

class OpenposePoseExtractionService(PoseExtractionService):
    def get_players_from_frame(self, frame):
        # FIXME
        return {
            'top': None,
            'bottom': None
        }
