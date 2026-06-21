from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ViolationResult:
    violation_type: str
    confidence: float
    bbox: List[int] # [x1, y1, x2, y2] of the violating object (e.g. the vehicle)
    explanation: str
    track_id: Optional[int] = None
    extra_data: Optional[Dict[str, Any]] = None

class ViolationRule(ABC):
    @abstractmethod
    def detect(self, frame: Any, detections: List[Dict[str, Any]], context: Dict[str, Any]) -> List[ViolationResult]:
        """
        Takes the current frame, a list of detections (or tracked objects),
        and contextual config (e.g., ROIs, allowed directions).
        Returns a list of ViolationResults.
        """
        pass
