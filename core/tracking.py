
import time
from collections import deque

class SimpleTracker:
    def __init__(self, maxlen=10):
        self.history = deque(maxlen=maxlen)

    def update(self, cx, cy):
        now = time.time()
        self.history.append((now, float(cx), float(cy)))

    def last(self):
        if not self.history:
            return None
        return self.history[-1]

    def velocity_px_per_s(self):
        if len(self.history) < 2:
            return (0.0, 0.0)
        t1, x1, y1 = self.history[-2]
        t2, x2, y2 = self.history[-1]
        dt = t2 - t1
        if dt <= 0:
            return (0.0, 0.0)
        vx = (x2 - x1) / dt
        vy = (y2 - y1) / dt
        return (vx, vy)

    def is_stable(self, px_thresh=5.0, time_window=0.2):
        import time
        now = time.time()
        pts = [p for p in self.history if now - p[0] <= time_window]
        if len(pts) < 2:
            return False
        xs = [p[1] for p in pts]
        ys = [p[2] for p in pts]
        return (max(xs)-min(xs) <= px_thresh) and (max(ys)-min(ys) <= px_thresh)
