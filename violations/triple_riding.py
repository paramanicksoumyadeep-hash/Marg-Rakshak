from typing import List, Dict, Any
from violations.base import ViolationRule, ViolationResult

class TripleRidingViolation(ViolationRule):
    def detect(self, frame: Any, detections: List[Dict[str, Any]], context: Dict[str, Any]) -> List[ViolationResult]:
        results = []
        
        riders = [d for d in detections if d.get('class_name') == 'rider']
        motorcycles = [d for d in detections if d.get('class_name') == 'motorcycle']
        
        for moto in motorcycles:
            mx1, my1, mx2, my2 = moto['bbox']
            moto_area = (mx2 - mx1) * (my2 - my1)
            
            associated_riders = 0
            rider_confidences = []
            
            for rider in riders:
                rx1, ry1, rx2, ry2 = rider['bbox']
                
                # Check overlap of rider with motorcycle
                x_left = max(rx1, mx1)
                y_top = max(ry1, my1)
                x_right = min(rx2, mx2)
                y_bottom = min(ry2, my2)
                
                if x_right > x_left and y_bottom > y_top:
                    inter_area = (x_right - x_left) * (y_bottom - y_top)
                    rider_area = (rx2 - rx1) * (ry2 - ry1)
                    
                    # If rider is mostly overlapping with the motorcycle box
                    if inter_area / float(rider_area) > 0.3:
                        associated_riders += 1
                        rider_confidences.append(rider['confidence'])
                        
            if associated_riders > 2:
                avg_conf = sum(rider_confidences) / len(rider_confidences)
                results.append(ViolationResult(
                    violation_type="Triple riding",
                    confidence=avg_conf,
                    bbox=moto['bbox'],
                    explanation=f"{associated_riders} riders detected on a single two-wheeler.",
                    track_id=moto.get('track_id')
                ))
                
        return results
