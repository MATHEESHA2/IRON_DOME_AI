
# control/pi_controller.py
# Simple Pi controller stub: listens for commands over serial or TCP and forwards to Arduino.
# This is a template - adapt serial port names and GPIO/logic as needed.
import serial, time, argparse

def run_serial(port='/dev/ttyUSB0', baud=115200):
    ser = serial.Serial(port, baud, timeout=0.1)
    print('Opened serial', port)
    try:
        while True:
            line = ser.readline().decode(errors='ignore').strip()
            if line:
                print('RECV:', line)
            time.sleep(0.01)
    except KeyboardInterrupt:
        ser.close()

if __name__ == '__main__':
    run_serial()
