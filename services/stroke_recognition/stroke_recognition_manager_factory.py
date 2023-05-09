from .stroke_recognition_manager import StrokeRecognitionManager
from .mock_stroke_recognition_manager import MockStrokeRecognitionManager
from .dense_model_stroke_recognition_manager import DenseModelStrokeRecognitionManager


class StrokeRecognitionManagerFactory:
    def create(self) -> StrokeRecognitionManager:
        pass


class MockStrokeRecognitionManagerFactory(StrokeRecognitionManagerFactory):
    def create(self) -> MockStrokeRecognitionManager:
        return MockStrokeRecognitionManager()


class DenseModelStrokeRecognitionManagerFactory(StrokeRecognitionManagerFactory):
    def create(self) -> DenseModelStrokeRecognitionManager:
        return DenseModelStrokeRecognitionManager()
