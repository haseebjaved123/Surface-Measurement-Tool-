"""
Label images immediately - processes and labels all found images
"""
import os
import sys
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'

print("="*80)
print("LABELING IMAGES NOW")
print("="*80)

# Initialize
from main import IndustrialToolAnalyzer
analyzer = IndustrialToolAnalyzer()

# Find images in input_images folder
input_dir = "input_images"
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
    print(f"Created {input_dir} folder. Please add images there.")
    sys.exit(0)

import glob
images = []
for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.JPG', '*.JPEG', '*.PNG']:
    images.extend(glob.glob(os.path.join(input_dir, ext)))

if not images:
    print(f"No images in {input_dir} folder.")
    print("Please add your images to the 'input_images' folder.")
    sys.exit(0)

print(f"Found {len(images)} image(s) to label\n")

# Process each image
for i, img_path in enumerate(images, 1):
    print(f"[{i}/{len(images)}] Processing: {os.path.basename(img_path)}")
    try:
        result = analyzer.process_image(img_path)
        if result:
            dims = result.get('dimensions_extracted', [])
            if dims:
                print(f"  ✓ Labeled - Found {len(dims)} dimension(s):")
                for d in dims:
                    print(f"    • {d['value']} {d['unit']} ({d['value_mm']} mm)")
            else:
                print(f"  - No dimensions detected")
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:50]}")

print("\n" + "="*80)
print("LABELING COMPLETE!")
print("="*80)
print(f"Check 'output_images' folder for labeled images")
print(f"Check 'results' folder for detailed reports")
