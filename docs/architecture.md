
# System Architecture

- Laptop: runs YOLOv8 detection, MiDaS depth estimation, targeting math, and decides when to fire.
- Raspberry Pi: runs lightweight control script, relays commands to Arduino.
- Arduino Uno: controls servos (pan/tilt) and laser output. Enforces hardware safety interlock.
- Communication: Laptop -> Pi (serial or TCP), Pi -> Arduino (serial).
