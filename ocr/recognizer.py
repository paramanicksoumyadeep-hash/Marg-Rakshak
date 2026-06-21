import re
import logging
from typing import Tuple, Optional
import numpy as np

class LicensePlateRecognizer:
    def __init__(self, regex_pattern: str = "^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$", conf_thresh: float = 0.8):
        self.logger = logging.getLogger(__name__)
        self.regex = re.compile(regex_pattern)
        self.conf_thresh = conf_thresh
        
        try:
            import easyocr
            self.reader = easyocr.Reader(['en'], gpu=True)
            self.logger.info("Loaded EasyOCR for License Plate Recognition")
        except ImportError:
            self.logger.error("EasyOCR not installed. Falling back to stub OCR.")
            self.reader = None

    def recognize(self, plate_crop: np.ndarray) -> Tuple[Optional[str], float, bool]:
        """
        Runs OCR on the cropped license plate image.
        Returns: (extracted_text, confidence, is_valid_format)
        """
        if self.reader is None or plate_crop.size == 0:
            return None, 0.0, False
            
        results = self.reader.readtext(plate_crop)
        
        if not results:
            return None, 0.0, False
            
        # Extract the highest confidence result, or combine text
        # Usually plates might be split into multiple boxes if multi-line
        full_text = ""
        avg_conf = 0.0
        
        for bbox, text, conf in results:
            # Clean text (remove spaces, special characters)
            clean_text = re.sub(r'[^A-Z0-9]', '', text.upper())
            full_text += clean_text
            avg_conf += conf
            
        if not full_text:
            return None, 0.0, False
            
        avg_conf /= len(results)
        
        # Validate format
        is_valid = bool(self.regex.match(full_text))
        
        return full_text, avg_conf, is_valid
