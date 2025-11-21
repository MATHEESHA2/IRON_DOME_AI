import cv2
import asyncio

class PiCameraStreamer:
    def __init__(self, device=0, width=640, height=480, fps=30):
        self.cap = cv2.VideoCapture(device)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)

    async def stream(self, max_frames=120):
        cnt = 0
        loop = asyncio.get_event_loop()
        while cnt < max_frames:
            ret, frame = await loop.run_in_executor(None, self.cap.read)
            if not ret:
                break
            ret2, jpeg = cv2.imencode('.jpg', frame)
            if not ret2:
                break
            yield jpeg.tobytes()
            cnt += 1
        return

    def close(self):
        self.cap.release()
