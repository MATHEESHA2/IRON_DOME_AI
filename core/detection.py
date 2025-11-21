
from ultralytics import YOLO
import numpy as np
import cv2

class Detector:
    def __init__(self, model_path='models/yolov8n.pt', conf=0.35):
        self.model = YOLO(model_path)
        self.conf = conf

    def detect(self, frame):
        results = self.model(frame, conf=self.conf, verbose=False)
        dets = []
        if len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                cx = (x1 + x2) / 2.0
                cy = (y1 + y2) / 2.0
                dets.append({
                    'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                    'conf': conf, 'cls': cls, 'cx': cx, 'cy': cy
                })
        return dets

    @staticmethod
    def draw_detections(frame, dets):
        out = frame.copy()
        for d in dets:
            x1,y1,x2,y2 = map(int, (d['x1'], d['y1'], d['x2'], d['y2']))
            cv2.rectangle(out, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(out, f"{d['conf']:.2f}", (x1, y1-6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        return out
