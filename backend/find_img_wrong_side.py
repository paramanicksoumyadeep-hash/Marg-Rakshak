import os
import shutil
from ultralytics import YOLO

model = YOLO('E:/flipkarttrafficapp/runs (2)/runs/detect/weights/eagle_eye_v1/weights/best.pt')
img_dir = 'E:/flipkarttrafficapp/datasets/Wrong Way Driving Detection.v1i.yolov11/valid/images'
found = False
count = 0

if os.path.exists(img_dir):
    for f in os.listdir(img_dir):
        if f.endswith('.jpg'):
            p = os.path.join(img_dir, f)
            res = model(p, conf=0.25, verbose=False)
            classes = res[0].boxes.cls.cpu().numpy()
            
            # 21 is wrong_side_vehicle
            if 21 in classes:
                print('Found wrong_side_vehicle in:', f)
                shutil.copy(p, 'E:/flipkarttrafficapp/video/demo_perfect_wrong_side.jpg')
                found = True
                break
            
            count += 1
            if count > 200:
                break

if not found:
    print('Could not find any wrong_side_vehicle in first 200 images')

# For illegal parking, just copy one since the model doesn't have that class
park_dir = 'E:/flipkarttrafficapp/datasets/Illegal Parking.v1i.yolov11/valid/images'
if os.path.exists(park_dir):
    for f in os.listdir(park_dir):
        if f.endswith('.jpg'):
            shutil.copy(os.path.join(park_dir, f), 'E:/flipkarttrafficapp/video/demo_illegal_parking.jpg')
            print('Copied demo_illegal_parking.jpg')
            break
