"""
Example script to test the OCR system
"""
from main import IndustrialToolAnalyzer
import os

def test_system():
    """
    Test the OCR system with example workflow
    """
    print("="*80)
    print("INDUSTRIAL TOOL OCR DIMENSION DETECTION - TEST SCRIPT")
    print("="*80)
    
    analyzer = IndustrialToolAnalyzer()
    
    # Check if input directory exists and has images
    if os.path.exists("input_images") and os.listdir("input_images"):
        print("\nFound images in input_images/ directory")
        print("Processing all images...\n")
        
        results = analyzer.process_directory("input_images")
        
        if results:
            print(f"\n{'='*80}")
            print(f"Successfully processed {len(results)} image(s)")
            print(f"{'='*80}")
            
            # Save results
            analyzer.save_results(results)
            analyzer.generate_report(results)
            
            # Print summary
            print("\nSUMMARY:")
            for i, result in enumerate(results, 1):
                print(f"\nImage {i}: {os.path.basename(result['image_path'])}")
                print(f"  Dimensions found: {len(result['dimensions_extracted'])}")
                for dim in result['dimensions_extracted']:
                    print(f"    - {dim['value']} {dim['unit']} ({dim['value_mm']} mm)")
                
                if result['calculations']:
                    for calc in result['calculations']:
                        print(f"  Surface Area ({calc['shape']}): {calc['total_area_cm2']:.2f} cm²")
        else:
            print("No results generated. Please check your images.")
    else:
        print("\nNo images found in input_images/ directory.")
        print("Please add images to the 'input_images/' folder and run again.")
        print("\nExample usage:")
        print("  python main.py --image path/to/image.jpg")
        print("  python main.py --dir path/to/images/")

if __name__ == "__main__":
    test_system()
