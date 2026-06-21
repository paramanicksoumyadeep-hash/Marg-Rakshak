import os
import shutil
from ultralytics import YOLO

model = YOLO('E:/flipkarttrafficapp/runs (2)/runs/detect/weights/eagle_eye_v1/weights/best.pt')
img_dir = 'E:/flipkarttrafficapp/datasets/Indian Number Plates.yolov11/valid/images'
found = False

if os.path.exists(img_dir):
    for f in os.listdir(img_dir):
        if f.endswith('.jpg'):
            p = os.path.join(img_dir, f)
            res = model(p, conf=0.10, verbose=False) # extremely low confidence just to find anything
            classes = res[0].boxes.cls.cpu().numpy()
            
            # 10 is license_plate
            if 10 in classes:
                print('Found license_plate in:', f)
                shutil.copy(p, 'E:/flipkarttrafficapp/video/demo_perfect_license_plate.jpg')
                found = True
                break

if not found:
    # Try training set if valid failed
    train_dir = 'E:/flipkarttrafficapp/datasets/Indian Number Plates.yolov11/train/images'
    if os.path.exists(train_dir):
        for f in os.listdir(train_dir):
            if f.endswith('.jpg'):
                p = os.path.join(train_dir, f)
                res = model(p, conf=0.10, verbose=False)
                classes = res[0].boxes.cls.cpu().numpy()
                if 10 in classes:
                    print('Found license_plate in train set:', f)
                    shutil.copy(p, 'E:/flipkarttrafficapp/video/demo_perfect_license_plate.jpg')
                    found = True
                    break

if not found:
    print('Could not find any license_plate in all images')
