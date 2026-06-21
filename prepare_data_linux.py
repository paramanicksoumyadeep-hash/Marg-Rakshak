#!/usr/bin/env python3
import os
import shutil
import json
import yaml
from glob import glob
from tqdm import tqdm

def load_mapping(path="data/universal_mapping.json"):
    with open(path, 'r') as f:
        return json.load(f)

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
                
                # Use hash to prevent "Filename too long" errors (ENAMETOOLONG) on Linux
                import hashlib
                short_hash = hashlib.md5(base_name.encode('utf-8')).hexdigest()[:12]
                
                safe_ds_name = ds_name.replace(" ", "_").replace(".", "_")
                # Keep it reasonably short
                short_ds_name = safe_ds_name[:20]
                
                new_base_name = f"{short_ds_name}_{short_hash}"
                
                new_img_name = f"{new_base_name}{img_ext}"
                new_lbl_name = f"{new_base_name}.txt"
                
                out_img_path = os.path.join(out_dir, split, "images", new_img_name)
                out_lbl_path = os.path.join(out_dir, split, "labels", new_lbl_name)
                
                # Copy image
                try:
                    shutil.copy(img_path, out_img_path)
                except FileNotFoundError:
                    continue
                total_images_processed += 1
                
                # Rewrite labels if they exist
                if os.path.exists(lbl_path):
                    with open(lbl_path, 'r') as lf:
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
                            
                    with open(out_lbl_path, 'w') as out_lf:
                        out_lf.writelines(new_lines)

    print(f"\nTotal images merged: {total_images_processed}")

    # Create merged data.yaml
    # Convert string keys to int and sort them, to get the correct ordered names list
    max_idx = max(int(k) for k in universal_classes.keys())
    names_list = []
    for i in range(max_idx + 1):
        names_list.append(universal_classes.get(str(i), f"unknown_{i}"))

    yaml_data = {
        "train": "train/images",
        "val": "valid/images",
        "test": "test/images",
        "nc": len(names_list),
        "names": names_list
    }
    
    with open(os.path.join(out_dir, "merged_data.yaml"), 'w') as f:
        yaml.dump(yaml_data, f, sort_keys=False)
        
    print(f"Created merged dataset at {out_dir}/merged_data.yaml")

if __name__ == "__main__":
    prepare_merged_dataset()
