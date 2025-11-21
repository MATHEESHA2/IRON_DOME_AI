#!/usr/bin/env python3
import zmq, json, cv2, numpy as np
from inference.yolo_detector import YOLODetector
from inference.depth_estimator import MiDaSEstimator
from inference.tracker_kalman import Tracker

cfg = json.load(open('configs/zeromq_config.json')) if __import__('os').path.exists('configs/zeromq_config.json') else {'bind':'tcp://*:5555'}
ZMQ_ADDR = cfg.get('bind', 'tcp://*:5555')

print('Loading models...')
yolo = YOLODetector(weights_path='models/yolo/best.pt')
depth = MiDaSEstimator(model_path='models/depth/midas_small.onnx')
tracker = Tracker()

ctx = zmq.Context()
sock = ctx.socket(zmq.REP)
sock.bind(ZMQ_ADDR)
print('Listening on', ZMQ_ADDR)

while True:
    parts = sock.recv_multipart()
    meta = json.loads(parts[0].decode('utf-8'))
    jpg = parts[1]
    nparr = np.frombuffer(jpg, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    dets = yolo.detect(img)
    response = {'target_found': False}
    if len(dets) > 0:
        best = dets[0]
        bbox = best['bbox']
        x_center = int((bbox[0]+bbox[2])//2)
        y_center = int((bbox[1]+bbox[3])//2)
        depth_map = depth.estimate(img)
        h, w = depth_map.shape
        x = int(x_center * (w / img.shape[1]))
        y = int(y_center * (h / img.shape[0]))
        depth_cm = float(depth_map[y, x]) * 100.0
        tracker.update([x_center, y_center, depth_cm])
        response = {
            'target_found': True,
            'bbox': [x_center, y_center],
            'depth_cm': depth_cm,
            'class': best['class'],
            'confidence': float(best['conf']),
            'allow_fire': best['conf'] > 0.5
        }
    sock.send(json.dumps(response).encode('utf-8'))
