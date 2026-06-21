import os
import cv2
import yaml
import logging
from glob import glob
from tqdm import tqdm
import numpy as np

from preprocessing.enhancer import ImageEnhancer
from detection.engine import DetectionEngine
from detection.tracker import MultiObjectTracker
from ocr.recognizer import LicensePlateRecognizer
from evidence.generator import EvidenceGenerator

# Violations
from violations.helmet import HelmetViolation
from violations.triple_riding import TripleRidingViolation
from violations.seatbelt import SeatbeltViolation
from violations.stop_line import StopLineViolation
from violations.red_light import RedLightViolation
from violations.wrong_side import WrongSideViolation
from violations.parking import ParkingViolation

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("EaglesEye")

def load_config(path="configs/system.yaml"):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def run_batch_pipeline(image_dir: str, camera_id: str, config: dict):
    logger.info(f"Starting batch pipeline for camera {camera_id} on {image_dir}")
    
    # Initialize components
    enhancer = ImageEnhancer(
        clip_limit=config['preprocessing']['clahe_clip_limit'],
        tile_grid_size=tuple(config['preprocessing']['clahe_tile_grid_size'])
    )
    
    detector = DetectionEngine(
        model_path=config['detection']['model_path'],
        conf_thresh=config['pipeline']['confidence_threshold']
    )
    
    tracker = MultiObjectTracker(
        model_path=config['detection']['model_path'],
        tracker_type=config['tracking']['tracker_type']
    )
    
    ocr = LicensePlateRecognizer(
        regex_pattern=config['ocr']['plate_regex'],
        conf_thresh=config['ocr']['confidence_threshold']
    )
    
    evidence_gen = EvidenceGenerator()
    
    # Initialize rules
    rules = [
        HelmetViolation(),
        TripleRidingViolation(),
        SeatbeltViolation(),
        StopLineViolation(),
        RedLightViolation(),
        WrongSideViolation(),
        ParkingViolation()
    ]
    
    # Get sequential images (recursive to handle subfolders)
    image_files = []
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.PNG"]:
        image_files.extend(glob(os.path.join(image_dir, "**", ext), recursive=True))
    image_files = sorted(image_files)
    logger.info(f"Found {len(image_files)} images to process in {image_dir} and its subdirectories.")
    
    for img_path in tqdm(image_files, desc="Processing frames"):
        frame = cv2.imread(img_path)
        if frame is None:
            continue
            
        # 1. Preprocessing & Quality Check
        is_good, blur_score = enhancer.assess_quality(frame, config['preprocessing']['blur_variance_threshold'])
        if not is_good:
            logger.warning(f"Low quality frame skipped: {img_path} (score: {blur_score:.2f})")
            continue
            
        enhanced_frame = enhancer.enhance_frame(frame)
        
        # 2. Perception Core (Tracking gives us detections with IDs)
        tracked_objects = tracker.track_frame(enhanced_frame)
        if not tracked_objects:
            # Fallback to single frame detection if tracking model not loaded or empty
            tracked_objects = detector.detect(enhanced_frame)
            
        # 3. Violation Reasoning
        frame_violations = []
        camera_context = config.get('cameras', {}).get(camera_id, {})
        for rule in rules:
            violations = rule.detect(enhanced_frame, tracked_objects, camera_context)
            frame_violations.extend(violations)
            
        # 4. Identity Layer (OCR)
        for v in frame_violations:
            # If there's a violation, find the nearest license plate detection
            plates = [d for d in tracked_objects if d.get('class_name') == 'license_plate']
            
            if plates:
                # Find the plate that overlaps or is closest to the violating bounding box
                # Simple IoU/proximity logic
                best_plate = None
                best_dist = float('inf')
                vx1, vy1, vx2, vy2 = v.bbox
                vc_x, vc_y = (vx1+vx2)/2, (vy1+vy2)/2
                
                for p in plates:
                    px1, py1, px2, py2 = p['bbox']
                    pc_x, pc_y = (px1+px2)/2, (py1+py2)/2
                    dist = abs(vc_x - pc_x) + abs(vc_y - pc_y)
                    if dist < best_dist:
                        best_dist = dist
                        best_plate = p
                
                if best_plate:
                    px1, py1, px2, py2 = best_plate['bbox']
                    plate_crop = enhanced_frame[py1:py2, px1:px2]
                    plate_text, ocr_conf, is_valid = ocr.recognize(plate_crop)
                    
                    if not v.extra_data:
                        v.extra_data = {}
                    v.extra_data['plate_number'] = plate_text
                    
        # 5. Proof Layer
        if frame_violations:
            evidence_gen.create_evidence(enhanced_frame, tracked_objects, frame_violations, camera_id)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Eagle's Eye Batch Processor")
    parser.add_argument("--dir", type=str, default="datasets/riders_without_helmet", help="Directory containing images to process")
    args = parser.add_argument_args() if hasattr(parser, 'add_argument_args') else parser.parse_args()
    
    config = load_config()
    
    test_dir = args.dir
    os.makedirs(test_dir, exist_ok=True)
    
    # Check if directory has images, if not print instruction
    images = glob(os.path.join(test_dir, "*.*"))
    if not images:
        logger.info(f"Please place test images in {test_dir} and run this script again.")
        # create a dummy image to prevent crash on first run
        dummy = np.zeros((1080, 1920, 3), dtype=np.uint8)
        cv2.imwrite(os.path.join(test_dir, "dummy_frame.jpg"), dummy)
        
    run_batch_pipeline(test_dir, "cam_001_junction_A", config)
    logger.info("Batch processing complete.")
