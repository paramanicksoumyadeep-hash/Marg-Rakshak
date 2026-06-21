import logging
from typing import List, Dict, Any
import numpy as np
from ultralytics import YOLO

class MultiObjectTracker:
    def __init__(self, model_path: str, tracker_type: str = "bytetrack.yaml", conf_thresh: float = 0.25):
        """
        Initializes the tracking engine using ultralytics built-in tracking.
        tracker_type can be "bytetrack.yaml" or "botsort.yaml"
        """
        self.logger = logging.getLogger(__name__)
        self.tracker_type = tracker_type
        self.conf_thresh = conf_thresh
        
        try:
            self.model = YOLO(model_path)
            self.logger.info(f"Loaded tracking model from {model_path} with tracker {tracker_type}")
        except Exception as e:
            self.logger.error(f"Failed to load tracking model: {e}")
            self.model = None

    def track_frame(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Runs object tracking on a single frame.
        Expects frames to be passed sequentially.
        """
        if self.model is None:
            return []
            
        # Run tracking inference. persist=True tells the model this is part of a video sequence
        results = self.model.track(frame, persist=True, tracker=self.tracker_type, conf=self.conf_thresh, verbose=False)
        
        tracked_objects = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = float(box.conf[0].cpu().numpy())
                cls_id = int(box.cls[0].cpu().numpy())
                cls_name = result.names[cls_id]
                
                # Tracking ID might be None if the object is new or lost
                track_id = int(box.id[0].cpu().numpy()) if box.id is not None else -1
                
                tracked_objects.append({
                    "track_id": track_id,
                    "bbox": [int(x1), int(y1), int(x2), int(y2)],
                    "confidence": conf,
                    "class_id": cls_id,
                    "class_name": cls_name
                })
                
        return tracked_objects
