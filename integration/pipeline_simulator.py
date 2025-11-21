import cv2,time
from core.detection import Detector
from core.tracking import SimpleTracker
from core.targeting import Targeting

def main(source=0,model_path='models/yolov8n.pt'):
    cap=cv2.VideoCapture(source)
    if not cap.isOpened(): print('cannot open'); return
    frame_w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 1280)
    frame_h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 720)
    det=Detector(model_path)
    tracker=SimpleTracker()
    targeting=Targeting(frame_w,frame_h)
    while True:
        ret,frame=cap.read()
        if not ret: break
        dets=det.detect(frame)
        out=frame.copy()
        if dets:
            t=max(dets,key=lambda d:d['conf'])
            tracker.update(t['cx'],t['cy'])
            cv2.circle(out,(int(t['cx']),int(t['cy'])),6,(0,255,0),-1)
        cv2.imshow('sim',out)
        if cv2.waitKey(1)&0xFF==27: break
    cap.release(); cv2.destroyAllWindows()

if __name__=='__main__': main()
