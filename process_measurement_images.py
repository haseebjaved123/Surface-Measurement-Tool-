"""
Process measurement images and PPT images with annotations
"""
import os
import sys
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

import cv2
import numpy as np
from paddleocr import PaddleOCR
import re

print("="*80)
print("PROCESSING MEASUREMENT & PPT IMAGES WITH ANNOTATIONS")
print("="*80)
print()

# Initialize OCR
print("Initializing OCR...")
ocr = PaddleOCR(lang='en')
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

for img_file in os.listdir(input_dir):
    if any(target in img_file for target in target_images):
        img_path = os.path.join(input_dir, img_file)
        print(f"Processing: {img_file}")
        
        try:
            # Read image with Unicode support
            img_array = np.fromfile(img_path, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if img is None:
                print(f"  [ERROR] Could not read image")
                continue
            
            # Run OCR using predict method
            import tempfile
            temp_fd, temp_path = tempfile.mkstemp(suffix='.jpg')
            try:
                cv2.imwrite(temp_path, img)
                # Use predict instead of ocr
                try:
                    ocr_result = ocr.predict(temp_path)
                except:
                    # Fallback to ocr method
                    ocr_result = ocr.ocr(temp_path)
            finally:
                os.close(temp_fd)
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            
            # Extract dimensions
            dimensions = []
            all_text = []
            
            if ocr_result and ocr_result[0]:
                for line in ocr_result[0]:
                    if line:
                        bbox, (text, confidence) = line
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
                                dimensions.append({
                                    'value': value,
                                    'unit': unit,
                                    'text': text,
                                    'bbox': bbox,
                                    'confidence': confidence
                                })
            
            # Create annotated image
            annotated = img.copy()
            
            # Draw all text detections in yellow
            for text, conf, bbox in all_text:
                if conf > 0.3:
                    pts = np.array(bbox, dtype=np.int32)
                    cv2.polylines(annotated, [pts], True, (0, 255, 255), 2)  # Yellow
            
            # Draw dimension detections in green (thicker)
            for dim in dimensions:
                bbox = dim['bbox']
                pts = np.array(bbox, dtype=np.int32)
                # Green box for dimensions
                cv2.polylines(annotated, [pts], True, (0, 255, 0), 3)  # Green, thicker
                
                # Add label
                x, y = int(bbox[0][0]), int(bbox[0][1])
                label = f"{dim['value']} {dim['unit']}"
                (text_width, text_height), baseline = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
                )
                # Background for text
                cv2.rectangle(annotated, 
                             (x, y - text_height - 10), 
                             (x + text_width + 5, y), 
                             (0, 255, 0), -1)
                # Text
                cv2.putText(annotated, label, 
                           (x + 2, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (0, 0, 0), 2)
            
            # Save annotated image
            output_name = os.path.splitext(img_file)[0] + "_annotated.jpg"
            output_path = os.path.join("output_images", output_name)
            cv2.imwrite(output_path, annotated)
            
            print(f"  [OK] Found {len(dimensions)} dimension(s)")
            for dim in dimensions:
                print(f"      - {dim['value']} {dim['unit']} (confidence: {dim['confidence']:.2f})")
            print(f"  [OK] Saved: {output_path}")
            print()
            
            results.append({
                'image': img_file,
                'dimensions': dimensions,
                'output': output_path
            })
            
        except Exception as e:
            print(f"  [ERROR] {str(e)[:60]}")
            print()

print("="*80)
print("SUMMARY")
print("="*80)
print(f"Processed: {len(results)} images")
print(f"Total dimensions found: {sum(len(r['dimensions']) for r in results)}")
print()
print("Annotated images saved in: output_images/")
print("Green boxes = Detected dimensions")
print("Yellow boxes = All detected text")
