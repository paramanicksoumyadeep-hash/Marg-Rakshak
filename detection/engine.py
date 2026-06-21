import logging
from typing import List, Dict, Any
import numpy as np
import torch
from ultralytics import YOLO

class DetectionEngine:
    def __init__(self, model_path: str, conf_thresh: float = 0.25, iou_thresh: float = 0.45):
        """
        Initializes the YOLO model for perception.
        """
        self.logger = logging.getLogger(__name__)
        self.conf_thresh = conf_thresh
        self.iou_thresh = iou_thresh
        
        try:
            self.model = YOLO(model_path)
            self.logger.info(f"Loaded YOLO model from {model_path}")
            
            # Check device
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.logger.info(f"Using device: {self.device}")
            
        except Exception as e:
            self.logger.error(f"Failed to load YOLO model: {e}")
            # Stub model for compilation without actual weights during initial setup
            self.model = None

    def detect(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Runs object detection on a single frame.
        Returns a list of dictionaries with bounding box, class, and confidence.
        """
        if self.model is None:
            self.logger.warning("Model not loaded, returning empty detections.")
            return []
            
        # Run inference
        results = self.model(frame, conf=self.conf_thresh, iou=self.iou_thresh, verbose=False)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0].cpu().numpy())
                cls_id = int(box.cls[0].cpu().numpy())
                
                # Get class name
                cls_name = result.names[cls_id]
                
                detections.append({
                    "bbox": [int(x1), int(y1), int(x2), int(y2)],
                    "confidence": conf,
                    "class_id": cls_id,
                    "class_name": cls_name
                })
                
        return detections
