"""
Show summary of processed images
"""
import os
import json

print("="*80)
print("ANNOTATED IMAGES READY!")
print("="*80)
print()

output_dir = "output_images"
if os.path.exists(output_dir):
    images = [f for f in os.listdir(output_dir) if f.endswith('_annotated.jpg')]
    print(f"Found {len(images)} annotated images:")
    print()
    for img in sorted(images):
        print(f"  ✓ {img}")
    print()
    print("Location: output_images/ folder")
    print()
    print("Legend:")
    print("  - Green boxes = Detected dimensions (measurements)")
    print("  - Yellow boxes = All detected text")
    print("  - Labels show dimension values (e.g., '19 cm', '330 mm')")
    print()
    print("These images show:")
    print("  1. All text detected by OCR (yellow boxes)")
    print("  2. Dimensions specifically highlighted (green boxes)")
    print("  3. Dimension values labeled on the image")
else:
    print("No output images found yet. Processing may still be running.")
