
import cv2, time
from core.detection import Detector
from core.depth import DepthEstimator
from core.tracking import SimpleTracker
from core.targeting import Targeting

def main(source=0, model_path='models/yolov8n.pt', use_depth=False):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Cannot open video source", source)
        return
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 1280)
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 720)
    print("Frame size:", frame_w, frame_h)

    detector = Detector(model_path=model_path, conf=0.35)
    depth_model = DepthEstimator() if use_depth else None
    tracker = SimpleTracker()
    targeting = Targeting(frame_w, frame_h, hfov_deg=70.0, vfov_deg=43.0)

    sweep_angle = 30.0
    sweep_dir = 1
    locked = False
    lock_time = 0
    last_fire_time = 0
    FIRE_COOLDOWN = 1.0
    LATENCY = 0.12

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        dets = detector.detect(frame)
        target = None
        if dets:
            target = max(dets, key=lambda d: d['conf'])

        if not locked:
            sweep_angle += sweep_dir * 0.6
            if sweep_angle >= 150:
                sweep_angle = 150
                sweep_dir = -1
            if sweep_angle <= 30:
                sweep_angle = 30
                sweep_dir = 1

        display = frame.copy()
        status_txt = f"Sweep:{sweep_angle:.1f}°"

        if target is not None:
            tracker.update(target['cx'], target['cy'])
            vx_px_s, vy_px_s = tracker.velocity_px_per_s()
            deg_per_px = targeting.hfov / targeting.frame_w
            ang_vel_deg_s = vx_px_s * deg_per_px
            pan_offset, tilt_offset = targeting.pixel_to_offset_deg(target['cx'], target['cy'])
            desired_pan = sweep_angle + pan_offset
            lead_deg = targeting.compute_lead(ang_vel_deg_s, LATENCY)
            final_pan = desired_pan + lead_deg

            cv2.circle(display, (int(target['cx']), int(target['cy'])), 6, (0,255,0), -1)
            cv2.putText(display, f"conf:{target['conf']:.2f}", (int(target['x1']), int(target['y1'])-18),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.putText(display, f"pan_off:{pan_offset:.2f} tilt_off:{tilt_offset:.2f}", (10,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
            cv2.putText(display, f"desired_pan:{desired_pan:.1f} lead:{lead_deg:.2f} final:{final_pan:.1f}", (10,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

            stable = tracker.is_stable(px_thresh=10.0, time_window=0.25)
            if stable and target['conf']>0.5:
                if not locked:
                    print(f"[{time.time():.2f}] LOCK requested at pan {final_pan:.2f}")
                    locked = True
                    lock_time = time.time()
                else:
                    current_servo_angle = final_pan
                    ANGLE_TOL = 3.0
                    if abs(current_servo_angle - final_pan) <= ANGLE_TOL:
                        now = time.time()
                        if now - last_fire_time > FIRE_COOLDOWN:
                            print(f"[{now:.2f}] FIRE at pan {final_pan:.2f}")
                            last_fire_time = now
                            cv2.circle(display, (int(target['cx']), int(target['cy'])), 40, (0,0,255), 6)
        else:
            tracker.update(-1,-1)

        if locked and (time.time() - lock_time) > 1.0:
            locked = False

        cv2.putText(display, status_txt, (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
        cv2.imshow("Pipeline Simulator", display)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
