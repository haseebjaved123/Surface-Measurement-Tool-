"""
Simple script that makes it super easy to use - just double click or run this!
"""
import os
import sys
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'
from pathlib import Path

print("="*80)
print("INDUSTRIAL TOOL OCR DIMENSION DETECTOR")
print("="*80)
print()

# Create necessary directories
directories = ["input_images", "output_images", "processed_images", "results"]
for dir_name in directories:
    os.makedirs(dir_name, exist_ok=True)
    print(f"✓ Created/Checked directory: {dir_name}/")

print()

# Check if input_images has any images
input_dir = "input_images"
image_files = []
if os.path.exists(input_dir):
    for file in os.listdir(input_dir):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
            image_files.append(file)

if not image_files:
    print("⚠ No images found in 'input_images' folder!")
    print()
    print("INSTRUCTIONS:")
    print("1. Copy your industrial tool images to the 'input_images' folder")
    print("2. Run this script again (or double-click RUN.bat)")
    print()
    print("Supported formats: JPG, PNG, BMP, TIFF")
    print()
    input("Press Enter to exit...")
    sys.exit(0)

print(f"Found {len(image_files)} image(s) to process:")
for img in image_files:
    print(f"  - {img}")
print()

# Import and run the analyzer
try:
    from main import IndustrialToolAnalyzer
    
    print("Initializing OCR system...")
    print("(This may take a moment on first run - downloading models)")
    print()
    
    analyzer = IndustrialToolAnalyzer()
    
    print("Processing images...")
    print()
    
    results = analyzer.process_directory(input_dir)
    
    if results:
        print()
        print("="*80)
        print("SUCCESS! Processing Complete!")
        print("="*80)
        print()
        print(f"Processed {len(results)} image(s) successfully!")
        print()
        print("Results saved in:")
        print("  - output_images/  (images with detected dimensions)")
        print("  - results/        (JSON and text reports)")
        print()
        
        # Save results
        analyzer.save_results(results)
        analyzer.generate_report(results)
        
        print("SUMMARY:")
        print("-"*80)
        for i, result in enumerate(results, 1):
            img_name = os.path.basename(result['image_path'])
            print(f"\n{i}. {img_name}")
            print(f"   Dimensions found: {len(result['dimensions_extracted'])}")
            for dim in result['dimensions_extracted']:
                print(f"     • {dim['value']} {dim['unit']} ({dim['value_mm']} mm)")
            
            if result['calculations']:
                for calc in result['calculations']:
                    print(f"   Surface Area ({calc['shape']}): {calc['total_area_cm2']:.2f} cm²")
        
        print()
        print("="*80)
    else:
        print("⚠ No results generated. Please check your images.")
        
except Exception as e:
    print()
    print("="*80)
    print("ERROR occurred:")
    print(str(e))
    print("="*80)
    print()
    print("Please make sure:")
    print("1. All dependencies are installed (run: pip install -r requirements.txt)")
    print("2. Images are in the 'input_images' folder")
    print("3. Images are clear and have visible dimension labels")
    print()

input("Press Enter to exit...")
