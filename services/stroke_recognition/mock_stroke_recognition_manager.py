from .stroke_recognition_manager import StrokeRecognitionManager

class MockStrokeRecognitionManager(StrokeRecognitionManager):
    SEQUENCE_LENGTH = 10
    STROKE_COUNT = 7

    def __init__(self):
        self.idx = 0

    def handle_stroke(self, pose):
        stroke = (self.idx // MockStrokeRecognitionManager.SEQUENCE_LENGTH) % MockStrokeRecognitionManager.STROKE_COUNT
        self.idx += 1

        return stroke
