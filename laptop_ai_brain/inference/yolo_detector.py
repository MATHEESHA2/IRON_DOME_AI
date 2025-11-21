from ultralytics import YOLO

class YOLODetector:
    def __init__(self, weights_path='models/yolo/best.pt', img_size=640):
        try:
            self.model = YOLO(weights_path)
        except Exception as e:
            print('YOLO model load failed:', e)
            self.model = None
        self.img_size = img_size

    def detect(self, frame):
        if self.model is None:
            return []
        res = self.model.predict(frame, imgsz=self.img_size, conf=0.25, iou=0.45)
        if len(res) == 0:
            return []
        boxes = []
        r = res[0]
        for det in r.boxes:
            x1,y1,x2,y2 = det.xyxy[0].tolist()
            conf = float(det.conf[0])
            cls = int(det.cls[0])
            boxes.append({'bbox':[int(x1),int(y1),int(x2),int(y2)], 'conf':conf, 'class':cls})
        boxes = sorted(boxes, key=lambda x: -x['conf'])
        return boxes
