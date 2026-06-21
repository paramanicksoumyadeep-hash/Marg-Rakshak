import os
import shutil
import xml.etree.ElementTree as ET
from glob import glob
from tqdm import tqdm

# Original IDD Classes (we only care about the vehicles/people for our traffic system)
IDD_CLASSES = {
    "pedestrian": 0,
    "rider": 1,
    "car": 2,
    "truck": 3,
    "bus": 4,
    "motorcycle": 5,
    "bicycle": 6,
    "autorickshaw": 7
}

def convert_box(size, box):
    # Convert VOC bounding box to YOLO format
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_idd_to_yolo():
    base_dir = "datasets/idd/IDD_Detection"
    out_dir = "datasets/idd_yolo"
    
    # Text files contain lists of image names without extensions for each split
    splits = {
        "train": os.path.join(base_dir, "train.txt"),
        "valid": os.path.join(base_dir, "val.txt"),
        "test": os.path.join(base_dir, "test.txt")
    }
    
    for split_name, txt_file in splits.items():
        if not os.path.exists(txt_file):
            continue
            
        print(f"Converting {split_name} split...")
        os.makedirs(os.path.join(out_dir, split_name, "images"), exist_ok=True)
        os.makedirs(os.path.join(out_dir, split_name, "labels"), exist_ok=True)
        
        with open(txt_file, 'r') as f:
            image_names = [line.strip() for line in f.readlines()]
            
        for img_name in tqdm(image_names):
            xml_path = os.path.join(base_dir, "Annotations", f"{img_name}.xml")
            img_path = os.path.join(base_dir, "JPEGImages", f"{img_name}.jpg")
            
            if not os.path.exists(xml_path) or not os.path.exists(img_path):
                continue
                
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            size = root.find('size')
            w = int(size.find('width').text)
            h = int(size.find('height').text)
            
            yolo_labels = []
            
            for obj in root.iter('object'):
                difficult = obj.find('difficult')
                if difficult is not None and int(difficult.text) == 1:
                    continue
                    
                cls = obj.find('name').text.lower()
                if cls not in IDD_CLASSES:
                    continue
                    
                cls_id = IDD_CLASSES[cls]
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), 
                     float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                bb = convert_box((w, h), b)
                
                yolo_labels.append(f"{cls_id} {' '.join([str(a) for a in bb])}\n")
                
            if len(yolo_labels) > 0:
                # To bypass Windows max path, hash the name
                import hashlib
                short_hash = hashlib.md5(img_name.encode('utf-8')).hexdigest()[:12]
                
                dst_img = os.path.join(out_dir, split_name, "images", f"idd_{short_hash}.jpg")
                dst_lbl = os.path.join(out_dir, split_name, "labels", f"idd_{short_hash}.txt")
                
                # Prefix \\?\ for windows
                if os.name == 'nt':
                    src_img = '\\\\?\\' + os.path.abspath(img_path)
                    dst_img = '\\\\?\\' + os.path.abspath(dst_img)
                    dst_lbl = '\\\\?\\' + os.path.abspath(dst_lbl)
                else:
                    src_img = img_path
                
                shutil.copy(src_img, dst_img)
                with open(dst_lbl, 'w') as f:
                    f.writelines(yolo_labels)

if __name__ == "__main__":
    convert_idd_to_yolo()
    print("\nIDD Dataset successfully converted to YOLO format at datasets/idd_yolo!")
