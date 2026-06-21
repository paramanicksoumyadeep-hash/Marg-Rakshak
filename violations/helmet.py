from typing import List, Dict, Any
from violations.base import ViolationRule, ViolationResult

class HelmetViolation(ViolationRule):
    def detect(self, frame: Any, detections: List[Dict[str, Any]], context: Dict[str, Any]) -> List[ViolationResult]:
        results = []
        
        # Look for riders
        riders = [d for d in detections if d.get('class_name') == 'rider']
        no_helmets = [d for d in detections if d.get('class_name') == 'no_helmet']
        motorcycles = [d for d in detections if d.get('class_name') == 'motorcycle']
        
        # Simple IoU or bounding box inclusion check
        for rider in riders:
            rx1, ry1, rx2, ry2 = rider['bbox']
            
            # Check if there is a 'no_helmet' detection inside or overlapping heavily with the rider bbox
            for nh in no_helmets:
                nx1, ny1, nx2, ny2 = nh['bbox']
                
                # Check overlap
                x_left = max(rx1, nx1)
                y_top = max(ry1, ny1)
                x_right = min(rx2, nx2)
                y_bottom = min(ry2, ny2)
                
                if x_right > x_left and y_bottom > y_top:
                    # Intersection area
                    inter_area = (x_right - x_left) * (y_bottom - y_top)
                    nh_area = (nx2 - nx1) * (ny2 - ny1)
                    
                    if inter_area / float(nh_area) > 0.5:
                        # Found a rider without a helmet.
                        # Associate this rider with the nearest motorcycle
                        assoc_moto_bbox = rider['bbox'] # Fallback to rider bbox if no moto matched
                        if motorcycles:
                            # naive distance matching for prototype
                            assoc_moto = min(motorcycles, key=lambda m: abs(m['bbox'][0] - rx1) + abs(m['bbox'][1] - ry1))
                            assoc_moto_bbox = assoc_moto['bbox']

                        results.append(ViolationResult(
                            violation_type="Helmet non-compliance",
                            confidence=nh['confidence'],
                            bbox=assoc_moto_bbox,
                            explanation=f"Rider detected without a helmet (confidence: {nh['confidence']:.2f})",
                            track_id=rider.get('track_id')
                        ))
                        break
                        
        return results
