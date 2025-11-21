from filterpy.kalman import KalmanFilter
import numpy as np

class Tracker:
    def __init__(self):
        self.kf = KalmanFilter(dim_x=6, dim_z=3)
        dt = 0.1
        self.kf.F = np.array([[1,0,0,dt,0,0],[0,1,0,0,dt,0],[0,0,1,0,0,dt],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]])
        self.kf.H = np.array([[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0]])
        self.kf.P *= 10
        self.kf.R *= 5
        self.kf.Q *= 0.01
        self.initialized = False

    def update(self, meas):
        z = np.array(meas)
        if not self.initialized:
            self.kf.x[:3] = z.reshape((3,1))
            self.initialized = True
        else:
            self.kf.predict()
            self.kf.update(z)
        return self.kf.x
