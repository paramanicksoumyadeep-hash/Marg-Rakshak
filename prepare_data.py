import os
import shutil
import json
import yaml
from glob import glob
from tqdm import tqdm

def load_mapping(path="data/universal_mapping.json"):
    with open(path, 'r') as f:
        return json.load(f)

def get_long_path(path):
    abs_path = os.path.abspath(path)
    if os.name == 'nt' and not abs_path.startswith('\\\\?\\'):
        return '\\\\?\\' + abs_path
    return abs_path

def prepare_merged_dataset():
    mapping_data = load_mapping()
    universal_classes = mapping_data["universal_classes"]
    dataset_mappings = mapping_data["dataset_mappings"]
    
    base_in_dir = "datasets"
    out_dir = os.path.join(base_in_dir, "merged_dataset")
    
    splits = ["train", "valid", "test"]
    
    # Create output directories
    for split in splits:
        os.makedirs(os.path.join(out_dir, split, "images"), exist_ok=True)
        os.makedirs(os.path.join(out_dir, split, "labels"), exist_ok=True)
        
    total_images_processed = 0
        
    for ds_name, class_map in dataset_mappings.items():
        ds_path = os.path.join(base_in_dir, ds_name)
        if not os.path.exists(ds_path):
            print(f"Skipping {ds_name} - folder not found.")
            continue
            
        print(f"Processing dataset: {ds_name}")
        
        for split in splits:
            # Different datasets use 'val' or 'valid'. Check both.
            split_paths = [os.path.join(ds_path, split), os.path.join(ds_path, "val" if split == "valid" else split)]
            img_dir = None
            lbl_dir = None
            
            for sp in split_paths:
                if os.path.exists(os.path.join(sp, "images")):
                    img_dir = os.path.join(sp, "images")
                    lbl_dir = os.path.join(sp, "labels")
                    break
                    
            if not img_dir or not os.path.exists(img_dir):
                continue
                
            image_files = glob(os.path.join(img_dir, "*.*"))
            
            for img_path in tqdm(image_files, desc=f"  {split} split"):
                img_ext = os.path.splitext(img_path)[1]
                if img_ext.lower() not in ['.jpg', '.jpeg', '.png']:
                    continue
                    
                img_name = os.path.basename(img_path)
                base_name = os.path.splitext(img_name)[0]
                lbl_path = os.path.join(lbl_dir, f"{base_name}.txt")
                
                # To bypass Windows 260-character path limit, we hash the filename
                import hashlib
                short_hash = hashlib.md5(base_name.encode('utf-8')).hexdigest()[:12]
                
                new_img_name = f"{ds_name}_{short_hash}{img_ext}"
                new_lbl_name = f"{ds_name}_{short_hash}.txt"
                
                out_img_path = os.path.join(out_dir, split, "images", new_img_name)
                out_lbl_path = os.path.join(out_dir, split, "labels", new_lbl_name)
                
                # Bypass Windows path read limits
                src_img_long = get_long_path(img_path)
                dst_img_long = get_long_path(out_img_path)
                
                # Copy image
                try:
                    shutil.copy(src_img_long, dst_img_long)
                except FileNotFoundError:
                    continue
                total_images_processed += 1
                
                # Rewrite labels if they exist
                src_lbl_long = get_long_path(lbl_path)
                dst_lbl_long = get_long_path(out_lbl_path)
                
                if os.path.exists(src_lbl_long):
                    with open(src_lbl_long, 'r') as lf:
                        lines = lf.readlines()
                        
                    new_lines = []
                    for line in lines:
                        parts = line.strip().split()
                        if not parts:
                            continue
                            
                        orig_cls_id = parts[0]
                        
                        # Map to universal ID
                        if orig_cls_id in class_map:
                            new_cls_id = str(class_map[orig_cls_id])
                            parts[0] = new_cls_id
                            new_lines.append(" ".join(parts) + "\n")
                            
                    with open(dst_lbl_long, 'w') as out_lf:
                        out_lf.writelines(new_lines)

    print(f"\nTotal images merged: {total_images_processed}")

    # Create merged data.yaml
    yaml_data = {
        "train": "train/images",
        "val": "valid/images",
        "test": "test/images",
        "nc": len(universal_classes),
        "names": [universal_classes[str(i)] for i in range(len(universal_classes))]
    }
    
    with open(os.path.join(out_dir, "merged_data.yaml"), 'w') as f:
        yaml.dump(yaml_data, f, sort_keys=False)
        
    print(f"Created merged dataset at {out_dir}/merged_data.yaml")

if __name__ == "__main__":
    prepare_merged_dataset()
