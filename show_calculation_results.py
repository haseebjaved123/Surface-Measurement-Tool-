"""
Show calculation results summary
"""
import os
import json

print("="*80)
print("AUTOMATIC EQUIPMENT SURFACE AREA CALCULATION RESULTS")
print("="*80)
print()

output_dir = "output_images"
calculated_images = [f for f in os.listdir(output_dir) if f.endswith('_calculated.jpg')]

print(f"Found {len(calculated_images)} images with surface area calculations:")
print()

for img in sorted(calculated_images):
    print(f"  [OK] {img}")
    print(f"      Location: output_images/{img}")
    print()

print("="*80)
print("WHAT EACH IMAGE SHOWS:")
print("="*80)
print("1. Green measurement lines with arrows showing detected dimensions")
print("2. Calculation box displaying:")
print("   - Equipment Type (scoop, bucket, hopper, etc.)")
print("   - Detected Dimensions (e.g., '19 cm', '14 cm', '11 cm')")
print("   - Calculated Surface Area (in cm2 and m2)")
print()
print("Processing may still be running for remaining images...")
print("Check output_images/ folder for all results")
