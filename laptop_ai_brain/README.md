## Laptop AI Brain Setup
1. Create venv and install requirements: `pip install -r requirements.txt`
2. Download YOLOv8 weights and place them in `laptop_ai_brain/models/yolo/best.pt`.
3. Download MiDaS ONNX and place in `laptop_ai_brain/models/depth/midas_small.onnx`.
4. Run server: `python3 main_ai_server.py`

Notes: If models are missing, the server will run with fallbacks but detection will not work.
