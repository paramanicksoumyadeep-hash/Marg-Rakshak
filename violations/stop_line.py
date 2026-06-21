import cv2
import numpy as np
from typing import List, Dict, Any
from violations.base import ViolationRule, ViolationResult

class StopLineViolation(ViolationRule):
    def detect(self, frame: Any, detections: List[Dict[str, Any]], context: Dict[str, Any]) -> List[ViolationResult]:
        results = []
        
        # We need the stop line polygon from context
        # e.g. context['stop_line_polygon'] = [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        polygon_points = context.get('stop_line_polygon')
        if not polygon_points:
            return results
            
        poly = np.array(polygon_points, np.int32)
        vehicles = [d for d in detections if d.get('class_name') in ['car', 'motorcycle', 'bus', 'truck', 'auto']]
        
        for v in vehicles:
            vx1, vy1, vx2, vy2 = v['bbox']
            # Create a small polygon for the bottom-center of the vehicle (the wheels/front bumper area)
            v_bottom_center = (int((vx1 + vx2) / 2), vy2)
            
            # Check if the bottom center point is inside the stop line polygon
            # measure is >= 0 if inside
            is_inside = cv2.pointPolygonTest(poly, v_bottom_center, measureDist=False)
            
            if is_inside >= 0:
                results.append(ViolationResult(
                    violation_type="Stop-line violation",
                    confidence=v['confidence'],
                    bbox=v['bbox'],
                    explanation="Vehicle detected crossing the stop line ROI.",
                    track_id=v.get('track_id')
                ))
                
        return results
