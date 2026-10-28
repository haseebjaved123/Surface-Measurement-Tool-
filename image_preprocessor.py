"""
Enhanced image preprocessing module for optimal OCR results
"""
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import os

class ImagePreprocessor:
    def __init__(self):
        self.output_dir = "processed_images"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def preprocess(self, image_path, output_name=None):
        """
        Enhanced preprocessing pipeline for better OCR results
        """
        # Read image with Unicode path support
        try:
            img_array = np.fromfile(image_path, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is None:
                img = cv2.imread(image_path)
        except:
            img = cv2.imread(image_path)
        
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        original = img.copy()
        
        # Step 1: Resize if too small (improves OCR accuracy)
        height, width = img.shape[:2]
        min_dimension = 800
        if height < min_dimension or width < min_dimension:
            scale = max(min_dimension / height, min_dimension / width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        # Step 2: Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Step 3: Remove noise (multiple methods)
        # Bilateral filter to preserve edges while removing noise
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
        # Additional denoising for text-heavy images
        denoised = cv2.fastNlMeansDenoising(denoised, None, 10, 7, 21)
        
        # Step 4: Enhance contrast using CLAHE (adaptive histogram equalization)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        
        # Step 5: Gamma correction for better brightness
        gamma = 1.2
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        gamma_corrected = cv2.LUT(enhanced, table)
        
        # Step 6: Sharpening for text clarity
        kernel_sharpen = np.array([[-1, -1, -1],
                                   [-1,  9, -1],
                                   [-1, -1, -1]])
        sharpened = cv2.filter2D(gamma_corrected, -1, kernel_sharpen)
        
        # Step 7: Adaptive thresholding for text extraction
        binary = cv2.adaptiveThreshold(
            sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Step 8: Morphological operations to clean up
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        # Save processed image
        if output_name is None:
            output_name = os.path.basename(image_path)
        
        # Ensure .jpg extension for saving
        base_name = os.path.splitext(output_name)[0]
        output_path = os.path.join(self.output_dir, f"processed_{base_name}.jpg")
        cv2.imwrite(output_path, cleaned)
        
        # Also return enhanced color version for OCR (sometimes works better)
        enhanced_color = img.copy()
        return cleaned, original, enhanced_color
    
    def enhance_for_ocr(self, image):
        """
        Advanced enhancement specifically optimized for OCR
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Resize if too small (OCR works better on larger images)
        height, width = gray.shape
        min_size = 1000
        if height < min_size or width < min_size:
            scale = max(min_size / height, min_size / width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        # Advanced sharpening using unsharp masking
        gaussian = cv2.GaussianBlur(gray, (0, 0), 2.0)
        sharpened = cv2.addWeighted(gray, 1.5, gaussian, -0.5, 0)
        
        return sharpened
    
    def preprocess_multiple_versions(self, image_path):
        """
        Create multiple preprocessed versions and return the best one
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        versions = []
        
        # Version 1: High contrast grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
        v1 = clahe.apply(gray)
        versions.append(('high_contrast', v1))
        
        # Version 2: Inverted (for white text on dark background)
        v2 = cv2.bitwise_not(gray)
        versions.append(('inverted', v2))
        
        # Version 3: Adaptive threshold
        v3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
        versions.append(('adaptive_thresh', v3))
        
        # Version 4: Otsu threshold
        _, v4 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        versions.append(('otsu', v4))
        
        # Version 5: Denoised + enhanced
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        v5 = clahe.apply(denoised)
        versions.append(('denoised_enhanced', v5))
        
        return versions, img
