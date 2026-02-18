"""
Calculate equipment surface area and annotate with measurement lines and calculations
"""
import os
import sys
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

import cv2
import numpy as np
import easyocr
import re
import math
from smart_calculator import SmartCalculator

print("="*80)
print("AUTOMATIC EQUIPMENT SURFACE AREA CALCULATION")
print("="*80)
print()

# Initialize EasyOCR
print("Initializing OCR...")
reader = easyocr.Reader(['en'], gpu=False)
smart_calc = SmartCalculator()
print("Ready!")
print()

# Process measurement images (1-6) and PPT images (1-4)
target_images = []
for i in range(1, 7):
    target_images.append(f"measurment {i}_")
for i in range(1, 5):
    target_images.append(f"PPt{i}.png")

input_dir = "input_images"
os.makedirs("output_images", exist_ok=True)

results = []

def draw_measurement_line(img, pt1, pt2, label, color=(0, 255, 0), thickness=2):
    """Draw measurement line with arrow and label"""
    # Draw line
    cv2.line(img, pt1, pt2, color, thickness)
    
    # Draw arrows at both ends
    angle = math.atan2(pt2[1] - pt1[1], pt2[0] - pt1[0])
    arrow_length = 10
    
    # Arrow at pt1
    cv2.line(img, pt1, 
             (int(pt1[0] + arrow_length * math.cos(angle + math.pi - 0.5)),
              int(pt1[1] + arrow_length * math.sin(angle + math.pi - 0.5))),
             color, thickness)
    cv2.line(img, pt1,
             (int(pt1[0] + arrow_length * math.cos(angle + math.pi + 0.5)),
              int(pt1[1] + arrow_length * math.sin(angle + math.pi + 0.5))),
             color, thickness)
    
    # Arrow at pt2
    cv2.line(img, pt2,
             (int(pt2[0] + arrow_length * math.cos(angle - 0.5)),
              int(pt2[1] + arrow_length * math.sin(angle - 0.5))),
             color, thickness)
    cv2.line(img, pt2,
             (int(pt2[0] + arrow_length * math.cos(angle + 0.5)),
              int(pt2[1] + arrow_length * math.sin(angle + 0.5))),
             color, thickness)
    
    # Draw label
    mid_x, mid_y = (pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2
    (text_width, text_height), baseline = cv2.getTextSize(
        label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
    )
    # Background
    cv2.rectangle(img,
                 (mid_x - text_width // 2 - 5, mid_y - text_height - 10),
                 (mid_x + text_width // 2 + 5, mid_y + 5),
                 (255, 255, 255), -1)
    cv2.rectangle(img,
                 (mid_x - text_width // 2 - 5, mid_y - text_height - 10),
                 (mid_x + text_width // 2 + 5, mid_y + 5),
                 color, 2)
    # Text
    cv2.putText(img, label,
               (mid_x - text_width // 2, mid_y),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

for img_file in os.listdir(input_dir):
    if any(target in img_file for target in target_images):
        img_path = os.path.join(input_dir, img_file)
        print(f"Processing: {img_file}")
        
        try:
            # Read image
            img_array = np.fromfile(img_path, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if img is None:
                print(f"  [ERROR] Could not read image")
                continue
            
            # Run OCR
            ocr_result = reader.readtext(img_path)
            
            # Extract dimensions
            dimensions = []
            all_text = []
            
            for detection in ocr_result:
                bbox, text, confidence = detection
                all_text.append((text, confidence, bbox))
                
                # Find dimensions
                patterns = [
                    r'(\d+\.?\d*)\s*(cm|mm|m|CM|MM|M)\b',
                    r'(\d+\.?\d*)\s*x\s*(\d+\.?\d*)\s*(cm|mm|m|CM|MM|M)\b',
                ]
                
                for pattern in patterns:
                    matches = re.finditer(pattern, text, re.IGNORECASE)
                    for match in matches:
                        value = float(match.groups()[0])
                        unit = match.groups()[-1].lower() if match.groups()[-1] else 'mm'
                        
                        # Convert to mm
                        if unit == 'm':
                            value_mm = value * 1000
                        elif unit == 'cm':
                            value_mm = value * 10
                        else:
                            value_mm = value
                        
                        dimensions.append({
                            'value': value,
                            'value_mm': value_mm,
                            'unit': unit,
                            'text': text,
                            'bbox': bbox,
                            'confidence': confidence
                        })
            
            if not dimensions:
                print(f"  [INFO] No dimensions detected")
                continue
            
            # Calculate surface area
            calc_result = smart_calc.calculate_smart(dimensions, img_file)
            eq_type = smart_calc.identify_equipment_type(dimensions, img_file)
            
            # Create annotated image
            annotated = img.copy()
            h, w = annotated.shape[:2]
            
            # Draw measurement lines for dimensions
            line_idx = 0
            for dim in dimensions[:4]:  # Draw first 4 dimensions
                bbox = dim['bbox']
                # Get bbox center and edges
                x_coords = [pt[0] for pt in bbox]
                y_coords = [pt[1] for pt in bbox]
                center_x = int(sum(x_coords) / len(x_coords))
                center_y = int(sum(y_coords) / len(y_coords))
                
                # Draw measurement line (horizontal or vertical based on bbox orientation)
                bbox_width = max(x_coords) - min(x_coords)
                bbox_height = max(y_coords) - min(y_coords)
                
                if bbox_width > bbox_height:
                    # Horizontal line
                    pt1 = (center_x - 50, center_y)
                    pt2 = (center_x + 50, center_y)
                else:
                    # Vertical line
                    pt1 = (center_x, center_y - 50)
                    pt2 = (center_x, center_y + 50)
                
                label = f"{dim['value']} {dim['unit']}"
                draw_measurement_line(annotated, pt1, pt2, label, (0, 255, 0), 2)
                line_idx += 1
            
            # Draw calculation results box
            if calc_result:
                # Create info box
                box_y = 30
                box_height = 150
                cv2.rectangle(annotated, (10, box_y), (w - 10, box_y + box_height),
                             (255, 255, 255), -1)
                cv2.rectangle(annotated, (10, box_y), (w - 10, box_y + box_height),
                             (0, 255, 0), 3)
                
                # Title
                title = "AUTOMATIC EQUIPMENT SURFACE AREA CALCULATION"
                (tw, th), _ = cv2.getTextSize(title, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                cv2.putText(annotated, title, (w // 2 - tw // 2, box_y + 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                
                # Equipment type
                type_text = f"Equipment Type: {eq_type.upper()}"
                cv2.putText(annotated, type_text, (20, box_y + 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                
                # Dimensions
                dims_text = "Dimensions: " + ", ".join([f"{d['value']} {d['unit']}" for d in dimensions[:3]])
                cv2.putText(annotated, dims_text, (20, box_y + 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                
                # Surface area result
                area_text = f"Surface Area: {calc_result['total_area_cm2']:.2f} cm2 ({calc_result['total_area_m2']:.6f} m2)"
                cv2.putText(annotated, area_text, (20, box_y + 120),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 150, 0), 2)
            
            # Save annotated image
            output_name = os.path.splitext(img_file)[0] + "_calculated.jpg"
            output_path = os.path.join("output_images", output_name)
            cv2.imwrite(output_path, annotated)
            
            print(f"  [OK] Found {len(dimensions)} dimension(s)")
            for dim in dimensions:
                print(f"      - {dim['value']} {dim['unit']}")
            if calc_result:
                print(f"  [OK] Equipment Type: {eq_type}")
                print(f"  [OK] Surface Area: {calc_result['total_area_cm2']:.2f} cm2")
            print(f"  [OK] Saved: {output_path}")
            print()
            
            results.append({
                'image': img_file,
                'dimensions': dimensions,
                'calculation': calc_result,
                'equipment_type': eq_type,
                'output': output_path
            })
            
        except Exception as e:
            print(f"  [ERROR] {str(e)[:60]}")
            import traceback
            traceback.print_exc()
            print()

print("="*80)
print("SUMMARY")
print("="*80)
print(f"Processed: {len(results)} images")
print(f"Total dimensions found: {sum(len(r['dimensions']) for r in results)}")
print()
print("Annotated images with calculations saved in: output_images/")
print()
print("Each image shows:")
print("  - Green measurement lines with dimension labels")
print("  - Calculation box showing:")
print("    * Equipment Type")
print("    * Detected Dimensions")
print("    * Calculated Surface Area")
print()

# Show detailed results
for r in results:
    print(f"{r['image']}:")
    print(f"  Type: {r['equipment_type']}")
    print(f"  Dimensions: {len(r['dimensions'])}")
    if r['calculation']:
        print(f"  Surface Area: {r['calculation']['total_area_cm2']:.2f} cm2")
    print()
