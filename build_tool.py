"""
Build the complete Automatic Equipment Surface Area Calculation Tool
"""
import os
import sys
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'
# Fix Unicode encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from main import IndustrialToolAnalyzer
import glob
import json
from pathlib import Path

print("="*80)
print("AUTOMATIC EQUIPMENT SURFACE AREA CALCULATION TOOL")
print("="*80)
print()

# Initialize analyzer
print("Initializing OCR system...")
analyzer = IndustrialToolAnalyzer()
print("Ready!")
print()

# Find all images in input_images
input_dir = "input_images"
os.makedirs(input_dir, exist_ok=True)

image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', 
                    '*.JPG', '*.JPEG', '*.PNG', '*.BMP', '*.TIFF']

all_images = []
for ext in image_extensions:
    all_images.extend(glob.glob(os.path.join(input_dir, ext)))

if not all_images:
    print(f"No images found in {input_dir} folder.")
    print("Please add industrial tool images to the 'input_images' folder.")
    print()
    print("The tool will:")
    print("  1. Detect dimensions using OCR")
    print("  2. Identify equipment type")
    print("  3. Calculate surface area")
    print("  4. Generate labeled images and reports")
    sys.exit(0)

print(f"Found {len(all_images)} industrial tool image(s) to analyze")
print()

# Process all images
results = []
for i, img_path in enumerate(all_images, 1):
    try:
        img_name = os.path.basename(img_path)
        print(f"[{i}/{len(all_images)}] Analyzing: {img_name.encode('ascii', 'ignore').decode('ascii')}")
    except:
        print(f"[{i}/{len(all_images)}] Analyzing image {i}")
    try:
        result = analyzer.process_image(img_path, img_name)
        if result:
            results.append(result)
            dims = result.get('dimensions_extracted', [])
            if dims:
                print(f"  ✓ Detected {len(dims)} dimension(s)")
                for d in dims:
                    print(f"    - {d['value']} {d['unit']} ({d['value_mm']} mm)")
                
                # Show calculations
                for calc in result.get('calculations', []):
                    print(f"  ✓ Surface Area ({calc['shape']}): {calc['total_area_cm2']:.2f} cm²")
            else:
                print(f"  - No dimensions detected")
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:100]}")

print()

# Save comprehensive results
if results:
    analyzer.save_results(results, "equipment_analysis.json")
    analyzer.generate_report(results, "equipment_analysis_report.txt")
    
    print("="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print(f"Processed {len(results)} equipment image(s)")
    print()
    print("Results saved:")
    print("  → output_images/     - Labeled images with detected dimensions")
    print("  → results/equipment_analysis.json - Complete data")
    print("  → results/equipment_analysis_report.txt - Detailed report")
    print()
    
    # Summary
    print("SUMMARY:")
    print("-"*80)
    total_area = 0
    for result in results:
        img_name = os.path.basename(result['image_path'])
        print(f"\n{img_name}:")
        for calc in result.get('calculations', []):
            print(f"  Type: {calc['shape']}")
            print(f"  Surface Area: {calc['total_area_cm2']:.2f} cm²")
            total_area += calc['total_area_cm2']
    
    if total_area > 0:
        print(f"\nTotal Surface Area (all equipment): {total_area:.2f} cm²")
else:
    print("No results generated. Please check your images have visible dimension labels.")

print()
