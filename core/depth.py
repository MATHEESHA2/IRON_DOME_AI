
import torch
import cv2
import numpy as np

class DepthEstimator:
    def __init__(self, model_type="DPT_Large", device=None):
        self.device = device if device is not None else ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.hub.load("intel-isl/MiDaS", model_type)
        self.model.to(self.device)
        self.model.eval()
        self.transforms = torch.hub.load("intel-isl/MiDaS", "transforms").dpt_transform

    def predict(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        input_batch = self.transforms(img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            prediction = self.model(input_batch)
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze().cpu().numpy()
        return prediction

    @staticmethod
    def depth_at(depth_map, cx, cy):
        h, w = depth_map.shape
        x = int(np.clip(cx, 0, w-1))
        y = int(np.clip(cy, 0, h-1))
        return float(depth_map[y, x])
