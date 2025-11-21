
import math

class Targeting:
    def __init__(self, frame_w, frame_h, hfov_deg=70.0, vfov_deg=43.0):
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.hfov = hfov_deg
        self.vfov = vfov_deg

    def pixel_to_offset_deg(self, cx, cy):
        x_rel = (cx - self.frame_w / 2.0) / (self.frame_w / 2.0)
        y_rel = (cy - self.frame_h / 2.0) / (self.frame_h / 2.0)
        pan = x_rel * (self.hfov / 2.0)
        tilt = -y_rel * (self.vfov / 2.0)
        return pan, tilt

    def compute_lead(self, ang_vel_deg_s, latency_s):
        return ang_vel_deg_s * latency_s
