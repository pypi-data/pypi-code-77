import time
import collections


class FPSCounter:
    def __init__(self, avarageof=50):
        self.frametimestamps = collections.deque(maxlen=avarageof)

    def __call__(self):
        self.frametimestamps.append(time.time())
        if(len(self.frametimestamps) > 1):
            last = self.frametimestamps[-1]
            first = self.frametimestamps[0]
            return len(self.frametimestamps) / (last - first)
        else:
            return 0.0


class LimitFPS():
    def __init__(self, fps):
        self.time_0 = time.time()
        self.start = self.time_0
        self.fps = fps
        self.elapsed = 0

    def __call__(self):
        if time.time() >= self.time_0 + 1.0 / self.fps:
            self.time_0 = time.time()
            self.elapsed = self.time_0 - self.start
            return True
        return False

    def get_elapsed_seconds(self):
        return self.elapsed
