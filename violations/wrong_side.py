import math
from typing import List, Dict, Any
from violations.base import ViolationRule, ViolationResult

class WrongSideViolation(ViolationRule):
    def __init__(self):
        # Dictionary to store previous center points for each track_id to compute trajectory vector
        self.track_history = {}

    def detect(self, frame: Any, detections: List[Dict[str, Any]], context: Dict[str, Any]) -> List[ViolationResult]:
        results = []
        
        allowed_dir = context.get('allowed_direction') # e.g., [0, -1]
        tolerance = context.get('direction_tolerance_degrees', 45)
        
        if not allowed_dir:
            return results
            
        vehicles = [d for d in detections if d.get('class_name') in ['car', 'motorcycle', 'bus', 'truck', 'auto']]
        
        for v in vehicles:
            track_id = v.get('track_id')
            if track_id is None or track_id == -1:
                continue
                
            vx1, vy1, vx2, vy2 = v['bbox']
            center_x = (vx1 + vx2) / 2
            center_y = (vy1 + vy2) / 2
            
            if track_id in self.track_history:
                prev_x, prev_y = self.track_history[track_id]
                
                # Compute displacement vector
                dx = center_x - prev_x
                dy = center_y - prev_y
                
                # Only check if moved significantly (noise reduction)
                dist = math.hypot(dx, dy)
                if dist > 5.0:
                    # Angle of movement vs allowed angle
                    angle_movement = math.degrees(math.atan2(dy, dx))
                    angle_allowed = math.degrees(math.atan2(allowed_dir[1], allowed_dir[0]))
                    
                    angle_diff = abs((angle_movement - angle_allowed + 180) % 360 - 180)
                    
                    if angle_diff > (180 - tolerance): # moving completely opposite
                        results.append(ViolationResult(
                            violation_type="Wrong-side driving",
                            confidence=v['confidence'],
                            bbox=v['bbox'],
                            explanation=f"Trajectory angle {angle_movement:.1f} opposes allowed direction.",
                            track_id=track_id
                        ))
                        
            # Update history
            self.track_history[track_id] = (center_x, center_y)
            
        return results
