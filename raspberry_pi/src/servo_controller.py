try:
    import RPi.GPIO as GPIO
except Exception:
    # fallback for development machines
    class DummyGPIO:
        BCM = BOARD = OUT = LOW = HIGH = None
        def setmode(self, *a, **k): pass
        def setup(self, *a, **k): pass
        def PWM(self, *a, **k):
            class P:
                def start(self,*a,**k): pass
                def ChangeDutyCycle(self,*a,**k): pass
                def stop(self,*a,**k): pass
            return P()
        def cleanup(self): pass
    GPIO = DummyGPIO()
import time

class ServoController:
    def __init__(self, pulse_pin=18, min_duty=2.5, max_duty=12.5):
        GPIO.setmode(GPIO.BCM)
        self.pin = pulse_pin
        self.min = min_duty
        self.max = max_duty
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)

    def angle_to_duty(self, angle):
        return (self.min + (self.max - self.min) * (angle / 180.0))

    def move_to(self, angle, wait=0.2):
        angle = max(0, min(180, angle))
        duty = self.angle_to_duty(angle)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(wait)
        self.pwm.ChangeDutyCycle(0)

    def compute_angle_from_x(self, x_center, img_width=640, cam_fov_deg=62.0):
        rel = (x_center / img_width) - 0.5
        angle_offset = rel * cam_fov_deg
        current = 90 + angle_offset
        return max(0, min(180, current))

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
