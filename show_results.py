"""
Process one image and show the results
"""
import os
import sys
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

from main import IndustrialToolAnalyzer

print("Processing PPt1.png to show you the results...")
print()

analyzer = IndustrialToolAnalyzer()
result = analyzer.process_image("input_images/PPt1.png", "PPt1")

if result:
    print()
    print("="*80)
    print("RESULTS:")
    print("="*80)
    print(f"Dimensions found: {len(result['dimensions_extracted'])}")
    for dim in result['dimensions_extracted']:
        print(f"  - {dim['value']} {dim['unit']} ({dim['value_mm']} mm)")
    
    if result.get('calculations'):
        for calc in result['calculations']:
            print(f"\nSurface Area ({calc['shape']}):")
            print(f"  - {calc['total_area_cm2']:.2f} cm2")
            print(f"  - {calc['total_area_m2']:.6f} m2")
    
    print()
    print("Check these folders:")
    print("  - processed_images/processed_PPt1.jpg - Preprocessed image")
    print("  - output_images/PPt1_labeled.jpg - Labeled image with OCR results")
else:
    print("Failed to process image")
