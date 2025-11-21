
# GoldenDome Simulation - Software Repository
This repository contains the full software stack for the GoldenDome simulation prototype (software-first). 
It includes YOLOv8 detection, MiDaS depth estimation wrappers, a simple tracker, targeting math, a pipeline simulator, Pi/Arduino control stubs and documentation.

**Structure:** See `docs/architecture.md` for details.

**How to use (quick):**
1. Create Python venv, install requirements from `requirements.txt`.
2. Run `python integration/pipeline_simulator.py` to run the simulation (no hardware required).
3. Train YOLO with your dataset and replace `models/best.pt` or change model path in config.
4. Integrate with Pi/Arduino using `control/pi_controller.py` and `arduino/servo_laser.ino`

