import random
from typing import Dict, Any
from .base import PipelineTier

class MockPipeline(PipelineTier):
    def __init__(self):
        # Deterministic seed for repeatable demos
        random.seed(42)
        
    def detect(self, image_id: str, image_path: str) -> Dict[str, Any]:
        """
        Returns seeded synthetic detections matching the JSON schema.
        """
        # We vary the mock output slightly based on hash of image_id for determinism
        hash_val = hash(image_id) % 100
        
        plates = []
        violations = []
        vehicles = []
        
        # Simulate detection of a vehicle
        vehicles.append({
            "bbox": [100, 200, 300, 400],
            "vehicle_type": "two_wheeler",
            "confidence": 0.95,
            "source": "simulated"
        })
        
        # Simulate plate detection
        if hash_val < 80: # 80% chance to find a plate
            plate_text = f"KA01AB{1000 + hash_val}"
            plates.append({
                "text": plate_text,
                "bbox": [150, 350, 250, 380],
                "ocr_confidence": 0.92 if hash_val > 10 else 0.4, # Simulating illegible
                "source": "simulated"
            })
            
            # Simulate a violation
            v_types = ["helmet_non_compliance", "triple_riding", "wrong_side_driving", "red_light_violation", "stop_line_violation"]
            v_type = v_types[hash_val % len(v_types)]
            
            violations.append({
                "type": v_type,
                "bbox": [100, 200, 300, 400],
                "confidence": 0.88,
                "source": "simulated",
                "evidence_crop_url": f"/evidence/{image_id}_crop.jpg"
            })

        return {
            "image_id": image_id,
            "vehicles": vehicles,
            "violations": violations,
            "plates": plates
        }
