try:
    import RPi.GPIO as GPIO
except Exception:
    class GPIO:
        BCM = OUT = HIGH = LOW = None
        def setmode(self,*a,**k): pass
        def setup(self,*a,**k): pass
        def output(self,*a,**k): pass

import time

class FiringSystem:
    def __init__(self, fire_pin=23, pulse_ms=100):
        self.pin = fire_pin
        self.pulse_ms = pulse_ms
        try:
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.LOW)
        except Exception:
            pass

    def trigger_pulse(self):
        try:
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(self.pulse_ms/1000.0)
            GPIO.output(self.pin, GPIO.LOW)
        except Exception:
            print('Simulated pulse (no GPIO available)')
