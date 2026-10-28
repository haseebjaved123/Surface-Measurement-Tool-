"""
Check all output images and list what's missing
"""
import os

output_dir = "output_images"
files = os.listdir(output_dir)
jpg_files = [f for f in files if f.endswith('.jpg')]

print("="*80)
print("OUTPUT IMAGES STATUS")
print("="*80)
print()

# Group by type
measurement_files = [f for f in jpg_files if 'measurement' in f.lower()]
ppt_files = [f for f in jpg_files if 'ppt' in f.lower()]

print("MEASUREMENT IMAGES:")
print("-" * 80)
for f in sorted(measurement_files):
    status = "CALCULATED" if "calculated" in f else "ANNOTATED"
    print(f"  {status:12} - {f}")

print()
print("PPT IMAGES:")
print("-" * 80)
for f in sorted(ppt_files):
    status = "CALCULATED" if "calculated" in f or "surface" in f else "ANNOTATED"
    print(f"  {status:12} - {f}")

print()
print("="*80)
print("SUMMARY:")
print("="*80)
print(f"Total images: {len(jpg_files)}")
print(f"  - Measurement: {len(measurement_files)}")
print(f"  - PPT: {len(ppt_files)}")
print()

# Check for missing calculated versions
annotated_only = [f for f in jpg_files if 'annotated' in f and 'calculated' not in f]
missing_calculated = []
for f in annotated_only:
    base = f.replace('_annotated.jpg', '')
    calculated = f"{base}_calculated.jpg"
    if calculated not in jpg_files and f"{base}_surface_area_calculated.jpg" not in jpg_files:
        missing_calculated.append(base)

if missing_calculated:
    print("MISSING CALCULATED VERSIONS:")
    for base in missing_calculated:
        print(f"  - {base}")
else:
    print("All annotated images have calculated versions!")
