from typing import List, Dict, Any
from abc import ABC, abstractmethod

class PipelineTier(ABC):
    @abstractmethod
    def detect(self, image_id: str, image_path: str) -> Dict[str, Any]:
        """
        Takes an image and returns the unified DetectionResult contract.
        """
        pass
