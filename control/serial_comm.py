
# control/serial_comm.py - simple sender for laptop to Pi or Arduino
import serial, time

class SerialClient:
    def __init__(self, port, baud=115200, timeout=0.1):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.ser = serial.Serial(port, baud, timeout=timeout)

    def send(self, msg):
        if not msg.endswith('\n'):
            msg = msg + '\n'
        self.ser.write(msg.encode())

    def close(self):
        self.ser.close()

if __name__ == '__main__':
    # example use
    c = SerialClient('/dev/ttyUSB0')
    c.send('PAN:90')
    time.sleep(0.1)
    c.send('FIRE')
    c.close()
