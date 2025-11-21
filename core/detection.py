from ultralytics import YOLO
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
                cx = (x1 + x2)/2.0
                cy = (y1 + y2)/2.0
                dets.append({'x1':x1,'y1':y1,'x2':x2,'y2':y2,'conf':conf,'cx':cx,'cy':cy})
        return dets
