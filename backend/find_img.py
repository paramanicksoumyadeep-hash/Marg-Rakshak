import os
import shutil
from ultralytics import YOLO

model = YOLO('E:/flipkarttrafficapp/runs (2)/runs/detect/weights/eagle_eye_v1/weights/best.pt')
img_dir = 'E:/flipkarttrafficapp/datasets/Triple Riding Model.v3i.yolov11/valid/images'
found = False
count = 0

for f in os.listdir(img_dir):
    if f.endswith('.jpg'):
        p = os.path.join(img_dir, f)
        res = model(p, conf=0.25, verbose=False)
        classes = res[0].boxes.cls.cpu().numpy()
        
        # 19 is triple_rider, 10 is license_plate. Let's find one that has both or at least 19
        if 19 in classes:
            print('Found triple_rider in:', f)
            shutil.copy(p, 'E:/flipkarttrafficapp/video/demo_perfect_triple_riding.jpg')
            found = True
            break
        
        count += 1
        if count > 200:
            break

if not found:
    print('Could not find any triple_rider in first 200 images')
