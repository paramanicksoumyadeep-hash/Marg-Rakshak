import cv2
import numpy as np

class ImageEnhancer:
    def __init__(self, clip_limit: float = 2.0, tile_grid_size: tuple = (8, 8)):
        """
        Initializes the Image Enhancer with CLAHE parameters.
        """
        self.clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)

    def enhance_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) to the image.
        Improves visibility in low light, fog, or glaring conditions.
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L-channel
        cl = self.clahe.apply(l)
        
        # Merge the CLAHE enhanced L-channel with the a and b channel
        limg = cv2.merge((cl, a, b))
        
        # Convert image from LAB Color model to BGR color space
        enhanced_frame = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return enhanced_frame

    def assess_quality(self, frame: np.ndarray, variance_threshold: float = 100.0) -> tuple[bool, float]:
        """
        Assesses image quality based on blurriness.
        Uses the variance of the Laplacian.
        
        Returns:
            Tuple[bool, float]: (is_good_quality, blur_score)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # If variance is less than threshold, it's considered blurry/low-confidence
        is_good_quality = blur_score > variance_threshold
        
        return is_good_quality, blur_score
