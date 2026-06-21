import cv2
import numpy as np
from typing import List, Dict, Any
from violations.base import ViolationRule, ViolationResult

class ParkingViolation(ViolationRule):
    def __init__(self):
        # Store how many frames a track_id has been stationary inside the ROI
        self.dwell_times = {}

    def detect(self, frame: Any, detections: List[Dict[str, Any]], context: Dict[str, Any]) -> List[ViolationResult]:
        results = []
        
        polygon_points = context.get('no_parking_polygon')
        max_dwell = context.get('parking_dwell_time_frames', 150)
        
        if not polygon_points:
            return results
            
        poly = np.array(polygon_points, np.int32)
        vehicles = [d for d in detections if d.get('class_name') in ['car', 'motorcycle', 'bus', 'truck', 'auto']]
        
        current_frame_tracks = set()
        
        for v in vehicles:
            track_id = v.get('track_id')
            if track_id is None or track_id == -1:
                continue
                
            current_frame_tracks.add(track_id)
                
            vx1, vy1, vx2, vy2 = v['bbox']
            center_point = (int((vx1 + vx2) / 2), int((vy1 + vy2) / 2))
            
            is_inside = cv2.pointPolygonTest(poly, center_point, measureDist=False)
            
            if is_inside >= 0:
                self.dwell_times[track_id] = self.dwell_times.get(track_id, 0) + 1
                
                if self.dwell_times[track_id] > max_dwell:
                    results.append(ViolationResult(
                        violation_type="Illegal parking",
                        confidence=v['confidence'],
                        bbox=v['bbox'],
                        explanation=f"Vehicle stationary in no-parking zone for {self.dwell_times[track_id]} frames.",
                        track_id=track_id
                    ))
            else:
                # If it left the zone, reset its dwell time
                if track_id in self.dwell_times:
                    del self.dwell_times[track_id]
                    
        # Cleanup lost tracks
        lost_tracks = set(self.dwell_times.keys()) - current_frame_tracks
        for t in lost_tracks:
            del self.dwell_times[t]
                
        return results
