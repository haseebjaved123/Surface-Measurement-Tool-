"""
Configuration file for OCR and dimension detection
"""
import os

# Paths
INPUT_DIR = "input_images"
OUTPUT_DIR = "output_images"
PROCESSED_DIR = "processed_images"
RESULTS_DIR = "results"

# OCR Settings
OCR_LANG = 'en'  # English
OCR_USE_ANGLE_CLS = True
OCR_USE_GPU = False  # Set to True if you have GPU

# Detection Settings
CONFIDENCE_THRESHOLD = 0.5
DIMENSION_PATTERNS = [
    r'(\d+\.?\d*)\s*(cm|mm|m)',  # Matches numbers with units
    r'(\d+\.?\d*)\s*(CM|MM|M)',  # Uppercase units
    r'(\d+\.?\d*)\s*x\s*(\d+\.?\d*)\s*(cm|mm|m)',  # Dimensions like "330mm x 270mm"
]

# Geometric shapes to detect
SHAPES = {
    'cylinder': ['diameter', 'height', 'radius'],
    'rectangular': ['length', 'width', 'height', 'depth'],
    'cone': ['top_diameter', 'bottom_diameter', 'height', 'slant_height'],
    'bucket': ['top_diameter', 'bottom_diameter', 'height'],
    'scoop': ['top_diameter', 'bottom_diameter', 'height'],
    'frustum': ['top_diameter', 'bottom_diameter', 'height', 'slant_height'],
}

# Create directories
for dir_path in [INPUT_DIR, OUTPUT_DIR, PROCESSED_DIR, RESULTS_DIR]:
    os.makedirs(dir_path, exist_ok=True)
