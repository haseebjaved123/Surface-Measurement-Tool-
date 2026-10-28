"""
Final processing script - processes all images and shows results
"""
import os
import sys
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from main import IndustrialToolAnalyzer
import glob
import json

print("="*80)
print("AUTOMATIC EQUIPMENT SURFACE AREA CALCULATION TOOL")
print("="*80)
print()

analyzer = IndustrialToolAnalyzer()

input_dir = "input_images"
images = []
for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.JPG', '*.JPEG', '*.PNG']:
    images.extend(glob.glob(os.path.join(input_dir, ext)))

print(f"Found {len(images)} images to process\n")

results = []
successful = 0
failed = 0

for i, img_path in enumerate(images, 1):
    try:
        img_name = os.path.basename(img_path)
        safe_name = img_name.encode('ascii', 'ignore').decode('ascii') or f"image_{i}"
        print(f"[{i}/{len(images)}] {safe_name[:40]}")
        
        result = analyzer.process_image(img_path, safe_name)
        if result:
            dims = result.get('dimensions_extracted', [])
            if dims:
                results.append(result)
                successful += 1
                print(f"  ✓ SUCCESS - {len(dims)} dimension(s) found")
                for d in dims[:3]:  # Show first 3
                    print(f"    • {d['value']} {d['unit']} ({d['value_mm']} mm)")
                for calc in result.get('calculations', []):
                    print(f"  ✓ Surface Area ({calc['shape']}): {calc['total_area_cm2']:.2f} cm²")
            else:
                failed += 1
                print(f"  - No dimensions detected")
        else:
            failed += 1
    except Exception as e:
        failed += 1
        print(f"  ✗ Error: {str(e)[:60]}")

print()
print("="*80)
print("PROCESSING COMPLETE")
print("="*80)
print(f"Successful: {successful}")
print(f"Failed: {failed}")
print()

if results:
    analyzer.save_results(results, "final_results.json")
    analyzer.generate_report(results, "final_report.txt")
    
    print("RESULTS SAVED:")
    print("  → output_images/ - Labeled images")
    print("  → results/final_results.json - Complete data")
    print("  → results/final_report.txt - Detailed report")
    print()
    print("SUMMARY:")
    print("-"*80)
    
    total_area = 0
    for result in results:
        img_name = os.path.basename(result['image_path'])
        safe_name = img_name.encode('ascii', 'ignore').decode('ascii') or "image"
        print(f"\n{safe_name[:50]}:")
        print(f"  Dimensions: {len(result['dimensions_extracted'])}")
        for calc in result.get('calculations', []):
            print(f"  {calc['shape'].upper()}: {calc['total_area_cm2']:.2f} cm² ({calc['total_area_m2']:.6f} m²)")
            total_area += calc['total_area_cm2']
    
    if total_area > 0:
        print(f"\nTOTAL SURFACE AREA: {total_area:.2f} cm² ({total_area/10000:.6f} m²)")
