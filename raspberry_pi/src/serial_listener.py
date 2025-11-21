import serial
import asyncio

class ArduinoSerialListener:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    async def listen(self):
        loop = asyncio.get_event_loop()
        while True:
            line = await loop.run_in_executor(None, self.ser.readline)
            if not line:
                await asyncio.sleep(0.01)
                continue
            try:
                s = line.decode('utf-8').strip()
            except Exception:
                continue
            if s.startswith('DETECTED'):
                parts = s.split(',')
                yield {'type':'DETECTED', 'angle':int(parts[1]), 'dist':int(parts[2])}
            elif s.startswith('HB'):
                parts = s.split(',')
                yield {'type':'HB', 'dist':int(parts[1])}
            else:
                yield {'type':'RAW', 'line':s}
