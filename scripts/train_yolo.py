
# scripts/train_yolo.py - helper to run YOLOv8 training
# Usage example (after dataset prepared):
# python scripts/train_yolo.py --data dataset/data.yaml --epochs 50 --img 640 --model yolov8n.pt
import argparse, subprocess

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data', default='dataset/data.yaml')
    p.add_argument('--epochs', type=int, default=50)
    p.add_argument('--img', type=int, default=640)
    p.add_argument('--model', default='yolov8n.pt')
    args = p.parse_args()
    cmd = ['yolo', 'task=detect', 'mode=train', f'model={args.model}', f'data={args.data}', f'epochs={args.epochs}', f'imgsz={args.img}']
    print('Running:', ' '.join(cmd))
    subprocess.run(cmd)

if __name__ == '__main__':
    main()
