from collections import deque

class StrokeRecognitionManager:
    MAX_QUEUE_SIZE = 4

    def __init__(self):
        self.queue = deque()

    def handle_stroke(self, pose):
        self.queue.append(pose)

        if len(self.queue) < self.MAX_QUEUE_SIZE:
            return None

        # TODO do recognition
        stroke = 1

        self.queue.popleft()

        return stroke
