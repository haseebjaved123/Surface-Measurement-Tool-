"""
Main pipeline for OCR-based dimension detection and surface area calculation
"""
import os
import sys

# Fix Windows encoding issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Avoid PaddleOCR/PaddlePaddle runtime issues with PIR/oneDNN on CPU.
os.environ.setdefault("FLAGS_use_mkldnn", "0")
os.environ.setdefault("FLAGS_enable_pir_api", "0")
os.environ.setdefault("FLAGS_enable_pir_in_executor", "0")
os.environ.setdefault("FLAGS_enable_pir", "0")
os.environ["DISABLE_MODEL_SOURCE_CHECK"] = "True"
import json
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict
import argparse

from image_preprocessor import ImagePreprocessor
from ocr_detector import OCRDetector
from geometry_calculator import GeometryCalculator
from config import *

class IndustrialToolAnalyzer:
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        self.ocr_detector = OCRDetector(lang=OCR_LANG, use_angle_cls=OCR_USE_ANGLE_CLS, use_gpu=OCR_USE_GPU)
        self.calculator = GeometryCalculator()
    
    def process_image(self, image_path: str, output_name: str = None) -> Dict:
        """
        Process a single image: preprocess, extract dimensions, calculate surface area
        """
        print(f"\n{'='*60}")
        print(f"Processing: {image_path}")
        print(f"{'='*60}")
        
        # Preprocess image with enhanced pipeline
        print("Step 1: Enhanced preprocessing...")
        try:
            processed_img, original_img, enhanced_color = self.preprocessor.preprocess(image_path, output_name)
            print("[OK] Image preprocessed with multiple enhancement techniques")
        except Exception as e:
            print(f"[ERROR] Preprocessing failed: {e}")
            return None
        
        # Extract dimensions using enhanced OCR
        print("Step 2: Extracting dimensions using enhanced OCR...")
        try:
            # Try with enhanced preprocessing first
            dimensions = self.ocr_detector.extract_dimensions(image_path, use_enhanced=True)
            
            if len(dimensions) == 0:
                # Fallback to standard extraction
                print("  Trying alternative preprocessing...")
                dimensions = self.ocr_detector.extract_dimensions(image_path, use_enhanced=False)
            
            print(f"[OK] Found {len(dimensions)} dimension(s)")
            for dim in dimensions:
                print(f"  - {dim['value']} {dim['unit']} ({dim['value_mm']} mm) - Confidence: {dim['confidence']:.2f}")
        except Exception as e:
            print(f"[ERROR] OCR extraction failed: {e}")
            return None
        
        # Enhanced visualization with dimension highlighting
        if output_name is None:
            output_name = Path(image_path).stem
        viz_path = os.path.join(OUTPUT_DIR, f"{output_name}_labeled.jpg")
        try:
            self.ocr_detector.visualize_results(image_path, viz_path, dimensions=dimensions)
            print(f"[OK] Enhanced labeled image saved to: {viz_path}")
        except Exception as e:
            print(f"[ERROR] Visualization failed: {e}")
        
        # Calculate surface area using smart calculator
        print("Step 3: Smart surface area calculation...")
        calculations = []
        
        if len(dimensions) >= 2:
            from smart_calculator import SmartCalculator
            smart_calc = SmartCalculator()
            
            img_name = os.path.basename(image_path)
            calc_result = smart_calc.calculate_smart(dimensions, img_name)
            
            if calc_result:
                calculations.append(calc_result)
                eq_type = smart_calc.identify_equipment_type(dimensions, img_name)
                print(f"[OK] Identified as: {eq_type}")
                print(f"[OK] Surface Area: {calc_result['total_area_cm2']:.2f} cm2 ({calc_result['total_area_m2']:.6f} m2)")
            else:
                # Fallback to basic calculation
                values_mm = [d['value_mm'] for d in dimensions]
                if len(dimensions) == 2:
                    diameter, height = max(values_mm), min(values_mm)
                    calc = self.calculator.calculate_cylinder_surface_area(diameter, height)
                    calculations.append(calc)
                    print(f"[OK] Calculated as cylinder: {calc['total_area_cm2']:.2f} cm2")
                elif len(dimensions) == 3:
                    length, width, height = values_mm[0], values_mm[1], values_mm[2]
                    calc = self.calculator.calculate_rectangular_surface_area(length, width, height)
                    calculations.append(calc)
                    print(f"[OK] Calculated as rectangular: {calc['total_area_cm2']:.2f} cm2")
        
        # Prepare result
        result = {
            'image_path': image_path,
            'dimensions_extracted': [
                {
                    'value': d['value'],
                    'unit': d['unit'],
                    'value_mm': d['value_mm'],
                    'confidence': d['confidence'],
                    'text': d['original_text']
                }
                for d in dimensions
            ],
            'calculations': calculations,
            'visualization_path': viz_path
        }
        
        return result
    
    def process_directory(self, input_dir: str) -> List[Dict]:
        """
        Process all images in a directory
        """
        results = []
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        
        for file in os.listdir(input_dir):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_path = os.path.join(input_dir, file)
                result = self.process_image(image_path, file)
                if result:
                    results.append(result)
        
        return results
    
    def save_results(self, results: List[Dict], output_file: str = "results.json"):
        """
        Save results to JSON file
        """
        output_path = os.path.join(RESULTS_DIR, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Results saved to: {output_path}")
    
    def generate_report(self, results: List[Dict], output_file: str = "report.txt"):
        """
        Generate a text report
        """
        output_path = os.path.join(RESULTS_DIR, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("INDUSTRIAL TOOL DIMENSION ANALYSIS REPORT\n")
            f.write("="*80 + "\n\n")
            
            for i, result in enumerate(results, 1):
                f.write(f"\nImage {i}: {result['image_path']}\n")
                f.write("-" * 80 + "\n")
                
                f.write("Extracted Dimensions:\n")
                for dim in result['dimensions_extracted']:
                    f.write(f"  • {dim['value']} {dim['unit']} ({dim['value_mm']} mm) "
                           f"[Confidence: {dim['confidence']:.2f}]\n")
                    f.write(f"    Text: {dim['text']}\n")
                
                f.write("\nSurface Area Calculations:\n")
                for calc in result['calculations']:
                    f.write(f"  Shape: {calc['shape']}\n")
                    f.write(f"  Total Area: {calc['total_area_mm2']:.2f} mm²\n")
                    f.write(f"  Total Area: {calc['total_area_cm2']:.2f} cm²\n")
                    f.write(f"  Total Area: {calc['total_area_m2']:.6f} m²\n")
                    f.write(f"  Dimensions: {calc['dimensions']}\n")
                
                f.write("\n")
        
        print(f"✓ Report saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Industrial Tool Dimension Detection and Surface Area Calculator')
    parser.add_argument('--image', type=str, help='Path to single image file')
    parser.add_argument('--dir', type=str, help='Path to directory containing images')
    parser.add_argument('--input-dir', type=str, default=INPUT_DIR, help='Default input directory')
    
    args = parser.parse_args()
    
    analyzer = IndustrialToolAnalyzer()
    
    if args.image:
        # Process single image
        result = analyzer.process_image(args.image)
        if result:
            analyzer.save_results([result], "single_result.json")
            analyzer.generate_report([result], "single_report.txt")
    elif args.dir:
        # Process directory
        results = analyzer.process_directory(args.dir)
        if results:
            analyzer.save_results(results)
            analyzer.generate_report(results)
    else:
        # Process default input directory
        if os.path.exists(INPUT_DIR) and os.listdir(INPUT_DIR):
            results = analyzer.process_directory(INPUT_DIR)
            if results:
                analyzer.save_results(results)
                analyzer.generate_report(results)
        else:
            print(f"Please place images in '{INPUT_DIR}' directory or use --image or --dir arguments")
            print(f"Created '{INPUT_DIR}' directory for you. Please add images and run again.")

if __name__ == "__main__":
    main()
