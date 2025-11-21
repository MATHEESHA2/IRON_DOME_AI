
# scripts/dataset_builder.py - simple helper to capture frames for dataset.
import cv2, os, time
out_dir = 'dataset/raw'
os.makedirs(out_dir, exist_ok=True)
cap = cv2.VideoCapture(0)
i = 0
print('Press s to save current frame, q to quit.')
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('capture', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        fn = os.path.join(out_dir, f'image_{i:04d}.jpg')
        cv2.imwrite(fn, frame)
        print('Saved', fn)
        i += 1
    elif key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
