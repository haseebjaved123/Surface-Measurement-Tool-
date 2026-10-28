"""
Process all images immediately with smart calculations
"""
import os
import sys
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'

# Fix Unicode
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from main import IndustrialToolAnalyzer
import glob

print("="*80)
print("PROCESSING ALL INDUSTRIAL TOOL IMAGES")
print("="*80)
print()

analyzer = IndustrialToolAnalyzer()

input_dir = "input_images"
images = []
for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.JPG', '*.JPEG', '*.PNG']:
    images.extend(glob.glob(os.path.join(input_dir, ext)))

print(f"Found {len(images)} images to process\n")

results = []
for i, img_path in enumerate(images, 1):
    try:
        img_name = os.path.basename(img_path)
        safe_name = img_name.encode('ascii', 'ignore').decode('ascii') or f"image_{i}"
        print(f"[{i}/{len(images)}] {safe_name}")
        
        result = analyzer.process_image(img_path, safe_name)
        if result and result.get('dimensions_extracted'):
            results.append(result)
            print(f"  ✓ Success - {len(result['dimensions_extracted'])} dimensions found")
            if result.get('calculations'):
                for calc in result['calculations']:
                    print(f"    Surface Area: {calc['total_area_cm2']:.2f} cm²")
        print()
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:80]}\n")

if results:
    analyzer.save_results(results, "equipment_analysis.json")
    analyzer.generate_report(results, "equipment_analysis_report.txt")
    print(f"\n✓ Processed {len(results)} images successfully!")
    print("Check output_images/ and results/ folders")
