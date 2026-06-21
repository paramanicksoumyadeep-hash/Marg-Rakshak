import cv2
import numpy as np
from typing import List, Dict, Any
from violations.base import ViolationRule, ViolationResult
from violations.stop_line import StopLineViolation

class RedLightViolation(ViolationRule):
    def __init__(self):
        self.stop_line_rule = StopLineViolation()

    def detect(self, frame: Any, detections: List[Dict[str, Any]], context: Dict[str, Any]) -> List[ViolationResult]:
        """
        Relies on the same spatial logic as Stop Line violation, but gated by the signal state.
        Signal state can be passed in context or detected via a signal state classifier on a ROI.
        """
        results = []
        
        # If signal state is not provided via IoT, we would run a basic color detector on the ROI
        signal_state = context.get('signal_state')
        roi = context.get('traffic_light_roi')
        
        if not signal_state and roi is not None:
            rx1, ry1, rx2, ry2 = roi
            light_crop = frame[ry1:ry2, rx1:rx2]
            if light_crop.size > 0:
                # Basic red color thresholding
                hsv = cv2.cvtColor(light_crop, cv2.COLOR_BGR2HSV)
                lower_red1 = np.array([0, 120, 70])
                upper_red1 = np.array([10, 255, 255])
                lower_red2 = np.array([170, 120, 70])
                upper_red2 = np.array([180, 255, 255])
                
                mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
                mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
                red_pixels = cv2.countNonZero(mask1 + mask2)
                
                # If a significant number of red pixels, assume red light
                if red_pixels > (light_crop.shape[0] * light_crop.shape[1] * 0.1):
                    signal_state = 'RED'
                else:
                    signal_state = 'GREEN'
                    
        if signal_state == 'RED':
            # Delegate to stop-line spatial logic
            stop_line_results = self.stop_line_rule.detect(frame, detections, context)
            for res in stop_line_results:
                results.append(ViolationResult(
                    violation_type="Red-light violation",
                    confidence=res.confidence,
                    bbox=res.bbox,
                    explanation="Vehicle crossed stop line while signal was RED.",
                    track_id=res.track_id
                ))
                
        return results
