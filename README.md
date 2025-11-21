# GOLDEN_DOME_AI

Automated target-intercept system: Arduino scanner -> Raspberry Pi targeting -> Laptop AI (YOLOv8 + MiDaS) -> Pi acts on confirmations.

**Important:** This repository provides complete code for devices and the AI server. It does NOT include large pretrained model binaries (YOLO weights, MiDaS ONNX). See `laptop_ai_brain/README.md` for download instructions.

**Safety:** Laser firing code is dangerous. Use passive safety measures and test without laser (set `--dry-run`) before enabling hardware.
