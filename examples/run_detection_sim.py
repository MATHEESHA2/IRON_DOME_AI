from core.detection import Detector
import cv2
m=Detector();cap=cv2.VideoCapture(0)
while True:
    r,f=cap.read()
    if not r: break
    dets=m.detect(f)
    out=f
    cv2.imshow('x',out)
    if cv2.waitKey(1)&0xFF==27: break
cap.release();cv2.destroyAllWindows()
