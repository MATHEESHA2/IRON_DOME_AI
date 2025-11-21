import onnxruntime as ort
import cv2
import numpy as np

class MiDaSEstimator:
    def __init__(self, model_path='models/depth/midas_small.onnx'):
        try:
            self.sess = ort.InferenceSession(model_path)
            self.input_name = self.sess.get_inputs()[0].name
        except Exception as e:
            print('MiDaS load failed:', e)
            self.sess = None

    def preprocess(self, img):
        h, w = img.shape[:2]
        img_in = cv2.resize(img, (256,256))
        img_in = img_in.astype('float32')/255.0
        img_in = img_in.transpose(2,0,1)[None,:,:,:]
        return img_in, (w,h)

    def estimate(self, img):
        if self.sess is None:
            h,w = img.shape[:2]
            return np.ones((h,w), dtype=float) * 0.5
        inp, (w,h) = self.preprocess(img)
        out = self.sess.run(None, {self.input_name: inp})[0]
        depth = out[0]
        depth = cv2.resize(depth, (w,h))
        depth = (depth - depth.min()) / (depth.max() - depth.min() + 1e-6)
        return depth
