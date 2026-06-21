from typing import Dict, Any
from .base import PipelineTier

class RealPipeline(PipelineTier):
    def __init__(self, model_path: str):
        # TODO: Initialize the real YOLO model here
        # self.model = YOLO(model_path)
        pass
        
    def detect(self, image_id: str, image_path: str) -> Dict[str, Any]:
        """
        Runs real YOLO inference.
        """
        # TODO: Run inference, format results matching the JSON contract
        raise NotImplementedError("Real adapter is stubbed out. Waiting for model weights.")
