import os
import cv2
import json
import hashlib
from datetime import datetime
import numpy as np
from typing import List, Dict, Any
from violations.base import ViolationResult

class EvidenceGenerator:
    def __init__(self, output_dir: str = "outputs/evidence"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_hash(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
        
    def apply_privacy_blur(self, frame: np.ndarray, detections: List[Dict[str, Any]], violating_bboxes: List[List[int]]) -> np.ndarray:
        """
        Blurs all plates and faces (riders/pedestrians) that are NOT part of a violation.
        """
        result_frame = frame.copy()
        
        privacy_classes = ['license_plate', 'rider', 'pedestrian', 'face']
        
        for det in detections:
            if det.get('class_name') in privacy_classes:
                x1, y1, x2, y2 = det['bbox']
                
                # Check if this bbox intersects significantly with any violating bbox
                is_violator = False
                for v_bbox in violating_bboxes:
                    vx1, vy1, vx2, vy2 = v_bbox
                    
                    # check intersection
                    ix1 = max(x1, vx1)
                    iy1 = max(y1, vy1)
                    ix2 = min(x2, vx2)
                    iy2 = min(y2, vy2)
                    
                    if ix2 > ix1 and iy2 > iy1:
                        is_violator = True
                        break
                        
                if not is_violator:
                    # Apply Gaussian blur to the region
                    roi = result_frame[y1:y2, x1:x2]
                    if roi.size > 0:
                        blurred_roi = cv2.GaussianBlur(roi, (51, 51), 0)
                        result_frame[y1:y2, x1:x2] = blurred_roi
                        
        return result_frame

    def create_evidence(self, frame: np.ndarray, detections: List[Dict[str, Any]], violations: List[ViolationResult], camera_id: str):
        """
        Generates the annotated image, applies privacy blur, and writes the metadata payload.
        """
        if not violations:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        base_filename = f"{camera_id}_{timestamp}"
        
        # 1. Apply privacy blur
        violating_bboxes = [v.bbox for v in violations]
        processed_frame = self.apply_privacy_blur(frame, detections, violating_bboxes)
        
        # 2. Draw annotations for the violations
        for v in violations:
            x1, y1, x2, y2 = v.bbox
            cv2.rectangle(processed_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            label = f"{v.violation_type} ({v.confidence:.2f})"
            cv2.putText(processed_frame, label, (x1, max(0, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            # Overlay explanation
            cv2.putText(processed_frame, v.explanation, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
        img_path = os.path.join(self.output_dir, f"{base_filename}.jpg")
        cv2.imwrite(img_path, processed_frame)
        
        frame_hash = self.generate_hash(img_path)
        
        # 3. Save metadata JSON
        metadata = {
            "evidence_id": base_filename,
            "camera_id": camera_id,
            "timestamp": datetime.now().isoformat(),
            "frame_hash": frame_hash,
            "violations": [
                {
                    "type": v.violation_type,
                    "confidence": v.confidence,
                    "explanation": v.explanation,
                    "plate_number": v.extra_data.get("plate_number") if v.extra_data else None,
                    "needs_human_review": v.confidence < 0.75 # Example config threshold
                } for v in violations
            ],
            "reviewer_status": "PENDING"
        }
        
        json_path = os.path.join(self.output_dir, f"{base_filename}.json")
        with open(json_path, "w") as f:
            json.dump(metadata, f, indent=4)
