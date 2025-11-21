import time
from collections import deque
class SimpleTracker:
    def __init__(self,maxlen=8): self.history=deque(maxlen=maxlen)
    def update(self,cx,cy): self.history.append((time.time(),float(cx),float(cy)))
    def velocity_px_per_s(self):
        if len(self.history)<2: return (0.0,0.0)
        t1,x1,y1=self.history[-2]; t2,x2,y2=self.history[-1]; dt=t2-t1
        if dt<=0: return (0.0,0.0)
        return ((x2-x1)/dt,(y2-y1)/dt)
    def is_stable(self,px_thresh=6.0,time_window=0.25):
        now=time.time(); pts=[p for p in self.history if now-p[0]<=time_window]
        if len(pts)<2: return False
        xs=[p[1] for p in pts]; ys=[p[2] for p in pts]
        return (max(xs)-min(xs)<=px_thresh) and (max(ys)-min(ys)<=px_thresh)
