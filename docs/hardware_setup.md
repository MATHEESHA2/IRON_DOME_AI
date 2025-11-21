
# Hardware Setup Notes

- Arduino pins: Pan servo -> D9, Tilt servo -> D10, Laser enable -> D7, Safety button -> D2 (INPUT_PULLUP)
- Power servos from separate 5V supply. Connect grounds.
- Pi connects to Arduino via USB serial (use Serial over USB).
- Use MOSFET to drive laser module from separate power if required.
