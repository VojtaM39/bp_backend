import keras
import tensorflow as tf
from collections import deque
from .stroke_recognition_manager import StrokeRecognitionManager
import numpy as np
from badminton_cv_utils.utils.pose_utils import get_normalized_pose


class DenseModelStrokeRecognitionManager(StrokeRecognitionManager):
    MAX_QUEUE_SIZE = 10
    DENSE_MODEL_PATH = '../../models/agg_model'

    def __init__(self):
        pass
        self.model = keras.models.load_model(DenseModelStrokeRecognitionManager.DENSE_MODEL_PATH)
        self.queue = deque()

    def handle_stroke(self, pose):
        if pose is None:
            return

        self.queue.append(pose)

        if len(self.queue) < self.MAX_QUEUE_SIZE:
            return None

        stroke = self.__evaluate_queue()
        self.queue.popleft()

        return stroke

    def __evaluate_queue(self):
        input = []
        for player in self.queue:
            normalized_player = get_normalized_pose(player)[:15]
            for point in normalized_player:
                input.append(point[0])
                input.append(point[1])

        input = tf.reshape(np.array(input), shape=(1, len(input)))
        pred = self.model(input, training=False)
        return int(np.argmax(pred))
