
# Basic detection test - ensures Detector import works
from core.detection import Detector
def test_detect_import():
    d = Detector(model_path='models/yolov8n.pt')
    assert d is not None
print('Detection test module loaded successfully.')
