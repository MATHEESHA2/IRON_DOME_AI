#!/usr/bin/env python3
import argparse
import asyncio
from serial_listener import ArduinoSerialListener
from camera_streamer import PiCameraStreamer
from zeromq_client import ZMQClient
from servo_controller import ServoController
from firing_system import FiringSystem
from safety_module import SafetyModule

async def main(args):
    ser = ArduinoSerialListener(args.serial_port)
    zmq = ZMQClient(args.zmq_server)
    cam = PiCameraStreamer()
    servo = ServoController(pulse_pin=args.servo_pin)
    fire = FiringSystem(fire_pin=args.fire_pin)
    safety = SafetyModule()

    print('Starting main loop')
    async for msg in ser.listen():
        print('Arduino:', msg)
        if msg.get('type') == 'DETECTED':
            async for frame in cam.stream(max_frames=80):
                resp = await zmq.send_frame(frame, metadata={'angle': msg['angle'], 'dist': msg['dist']})
                if resp.get('target_found'):
                    x_center = resp['bbox'][0]
                    depth_cm = resp['depth_cm']
                    target_angle = servo.compute_angle_from_x(x_center)
                    servo.move_to(target_angle)
                    if safety.is_safe_to_fire(depth_cm, resp):
                        if resp.get('allow_fire', False) and not args.dry_run:
                            fire.trigger_pulse()
                            print('FIRED')
                            break
                # continue

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial-port', default='/dev/ttyUSB0')
    parser.add_argument('--zmq-server', default='tcp://127.0.0.1:5555')
    parser.add_argument('--servo-pin', type=int, default=18)
    parser.add_argument('--fire-pin', type=int, default=23)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    asyncio.run(main(args))
