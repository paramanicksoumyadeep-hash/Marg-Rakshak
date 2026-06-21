from typing import List, Dict, Any
from violations.base import ViolationRule, ViolationResult

class SeatbeltViolation(ViolationRule):
    def detect(self, frame: Any, detections: List[Dict[str, Any]], context: Dict[str, Any]) -> List[ViolationResult]:
        results = []
        
        four_wheelers = [d for d in detections if d.get('class_name') in ['car', 'truck', 'bus']]
        no_seatbelts = [d for d in detections if d.get('class_name') == 'no_seatbelt']
        
        for fw in four_wheelers:
            fx1, fy1, fx2, fy2 = fw['bbox']
            
            for ns in no_seatbelts:
                nx1, ny1, nx2, ny2 = ns['bbox']
                
                # Check if no_seatbelt detection is inside the vehicle bbox
                x_left = max(fx1, nx1)
                y_top = max(fy1, ny1)
                x_right = min(fx2, nx2)
                y_bottom = min(fy2, ny2)
                
                if x_right > x_left and y_bottom > y_top:
                    inter_area = (x_right - x_left) * (y_bottom - y_top)
                    ns_area = (nx2 - nx1) * (ny2 - ny1)
                    
                    if inter_area / float(ns_area) > 0.5:
                        results.append(ViolationResult(
                            violation_type="Seatbelt non-compliance",
                            confidence=ns['confidence'],
                            bbox=fw['bbox'],
                            explanation=f"Occupant detected without a seatbelt inside the vehicle.",
                            track_id=fw.get('track_id')
                        ))
                        break # One violation per vehicle is enough for challan
                        
        return results
