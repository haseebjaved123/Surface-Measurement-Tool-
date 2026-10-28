"""
Fully automated script - processes all images automatically
Just run this and it will handle everything!
"""
import os
import sys
import time
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'

print("="*80)
print("AUTOMATED INDUSTRIAL TOOL OCR PROCESSOR")
print("="*80)
print()

# Create directories
directories = ["input_images", "output_images", "processed_images", "results"]
for dir_name in directories:
    os.makedirs(dir_name, exist_ok=True)

# Check for images
input_dir = "input_images"
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.JPG', '.JPEG', '.PNG', '.BMP', '.TIFF']

# Find all images
image_files = []
if os.path.exists(input_dir):
    for file in os.listdir(input_dir):
        if any(file.endswith(ext) for ext in image_extensions):
            image_files.append(os.path.join(input_dir, file))

if not image_files:
    print("No images found in 'input_images' folder.")
    print()
    print("Please add your images to the 'input_images' folder and run this script again.")
    print("Or drag and drop images into that folder, then run this script.")
    print()
    try:
        input("Press Enter to exit...")
    except:
        pass
    sys.exit(0)

print(f"Found {len(image_files)} image(s) to process:")
for img in image_files:
    print(f"  - {os.path.basename(img)}")
print()
print("Starting processing...")
print("(This may take a moment on first run - downloading OCR models)")
print()

try:
    from main import IndustrialToolAnalyzer
    
    # Initialize analyzer
    print("Initializing OCR system...")
    analyzer = IndustrialToolAnalyzer()
    print("Ready!")
    print()
    
    # Process all images
    all_results = []
    for i, image_path in enumerate(image_files, 1):
        print(f"[{i}/{len(image_files)}] Processing: {os.path.basename(image_path)}")
        try:
            result = analyzer.process_image(image_path, os.path.basename(image_path))
            if result:
                all_results.append(result)
                print(f"  ✓ Success!")
            else:
                print(f"  ✗ Failed to process")
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
        print()
    
    if all_results:
        # Save all results
        print("Saving results...")
        analyzer.save_results(all_results, "all_results.json")
        analyzer.generate_report(all_results, "complete_report.txt")
        
        print()
        print("="*80)
        print("PROCESSING COMPLETE!")
        print("="*80)
        print()
        print(f"Successfully processed {len(all_results)} image(s)")
        print()
        print("RESULTS:")
        print("-"*80)
        
        for i, result in enumerate(all_results, 1):
            img_name = os.path.basename(result['image_path'])
            print(f"\n{i}. {img_name}")
            print(f"   Dimensions found: {len(result['dimensions_extracted'])}")
            
            for dim in result['dimensions_extracted']:
                print(f"     • {dim['value']} {dim['unit']} ({dim['value_mm']} mm) [Confidence: {dim['confidence']:.2f}]")
            
            if result['calculations']:
                for calc in result['calculations']:
                    print(f"   Surface Area ({calc['shape']}):")
                    print(f"     - {calc['total_area_mm2']:.2f} mm²")
                    print(f"     - {calc['total_area_cm2']:.2f} cm²")
                    print(f"     - {calc['total_area_m2']:.6f} m²")
        
        print()
        print("="*80)
        print("FILES CREATED:")
        print("="*80)
        print("  → output_images/     - Images with detected dimensions labeled")
        print("  → processed_images/  - Enhanced/preprocessed images")
        print("  → results/           - JSON and text reports")
        print()
        print("Check these folders for all your results!")
        
    else:
        print("No images were successfully processed.")
        print("Please check that your images are clear and have visible dimension labels.")
        
except Exception as e:
    print()
    print("="*80)
    print("ERROR:")
    print("="*80)
    print(str(e))
    print()
    print("Please make sure all dependencies are installed.")
    print("If this is the first run, the OCR models are downloading (this is normal).")
    print()

print()
try:
    input("Press Enter to exit...")
except:
    pass
