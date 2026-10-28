"""
OCR module using PaddleOCR for dimension detection
"""
import os
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'
import re
import cv2
import numpy as np
from paddleocr import PaddleOCR
from typing import List, Dict, Tuple
import json

class OCRDetector:
    def __init__(self, lang='en', use_angle_cls=True, use_gpu=False):
        """
        Initialize PaddleOCR
        """
        print("Initializing PaddleOCR... This may take a moment on first run.")
        try:
            # Try new API first
            self.ocr = PaddleOCR(lang=lang)
        except:
            # Fallback to old API
            try:
                self.ocr = PaddleOCR(
                    use_angle_cls=use_angle_cls,
                    lang=lang
                )
            except:
                self.ocr = PaddleOCR(lang='en')
        self.dimension_patterns = [
            r'(\d+\.?\d*)\s*(cm|mm|m|CM|MM|M)',  # Simple dimension
            r'(\d+\.?\d*)\s*x\s*(\d+\.?\d*)\s*(cm|mm|m|CM|MM|M)',  # Multiple dimensions
            r'(\d+\.?\d*)\s*[xX×]\s*(\d+\.?\d*)\s*[xX×]?\s*(\d+\.?\d*)?\s*(cm|mm|m|CM|MM|M)?',  # 3D dimensions
        ]
    
    def extract_text(self, image_path: str, use_multiple_versions=False) -> List[Dict]:
        """
        Extract all text from image with bounding boxes
        Enhanced with multiple preprocessing versions for better accuracy
        """
        # Fix Unicode path issues
        try:
            # Try to read with proper encoding
            img_array = np.fromfile(image_path, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is None:
                # Fallback to regular read
                img = cv2.imread(image_path)
        except:
            img = cv2.imread(image_path)
        
        if img is None:
            return []
        
        # Save to temp file with ASCII name for OCR
        import tempfile
        temp_fd, temp_path = tempfile.mkstemp(suffix='.jpg')
        try:
            cv2.imwrite(temp_path, img)
            # Use temp file for OCR - simple call
            result = self.ocr.ocr(temp_path)
        finally:
            os.close(temp_fd)
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
        
        extracted_data = []
        if result and result[0]:
            for line in result[0]:
                if line:
                    bbox, (text, confidence) = line
                    # Filter low confidence results
                    if confidence > 0.3:  # Only keep results with >30% confidence
                        extracted_data.append({
                            'text': text,
                            'confidence': confidence,
                            'bbox': bbox
                        })
        
        return extracted_data
    
    def extract_dimensions(self, image_path: str, use_enhanced=True) -> List[Dict]:
        """
        Enhanced dimension extraction with better pattern matching
        """
        extracted_data = self.extract_text(image_path, use_multiple_versions=use_enhanced)
        dimensions = []
        seen_dimensions = set()  # Avoid duplicates
        
        # Enhanced patterns for better matching
        enhanced_patterns = [
            r'(\d+\.?\d*)\s*(cm|mm|m|CM|MM|M)\b',  # Simple dimension with word boundary
            r'(\d+\.?\d*)\s*x\s*(\d+\.?\d*)\s*(cm|mm|m|CM|MM|M)\b',  # Multiple dimensions
            r'(\d+\.?\d*)\s*[xX×]\s*(\d+\.?\d*)\s*[xX×]?\s*(\d+\.?\d*)?\s*(cm|mm|m|CM|MM|M)?\b',  # 3D dimensions
            r'(\d+\.?\d*)\s*(?:CM|MM|M)',  # Uppercase units
            r'(\d+\.?\d*)\s*(?:centimeter|millimeter|meter)',  # Full words
            r'\b(\d+\.?\d*)\b',  # Pure numbers (standalone) - assume cm for typical dimension values
        ]
        
        for item in extracted_data:
            text = item['text']
            # Clean text - remove common OCR errors but preserve Korean/Unicode characters
            # Only replace when it's clearly a mistake (not part of Korean text)
            original_text = text
            # Clean common OCR mistakes only for numeric patterns
            text_clean = text.replace('O', '0').replace('o', '0')  # Common OCR mistake
            text_clean = text_clean.replace('l', '1').replace('I', '1')  # Another common mistake
            
            # Try to match dimension patterns on cleaned text
            for pattern in enhanced_patterns:
                matches = re.finditer(pattern, text_clean, re.IGNORECASE)
                for match in matches:
                    groups = match.groups()
                    if len(groups) >= 1:
                        try:
                            # Extract numeric value and unit
                            value = float(groups[0])
                            
                            # Skip very small numbers that are likely not dimensions (confidence scores, indices)
                            # Also skip numbers in parentheses that look like confidence scores (e.g., "(1.00)")
                            if value < 2.0:
                                # Check if this number is in parentheses (likely a confidence score)
                                match_text = match.group()
                                if '(' in original_text and ')' in original_text:
                                    # Check if this match is inside parentheses
                                    match_start = original_text.find(match_text)
                                    if match_start > 0 and original_text[match_start-1] == '(':
                                        continue  # Skip confidence scores
                            
                            # Find unit
                            unit = None
                            for g in groups[1:]:
                                if g and g.lower() in ['cm', 'mm', 'm', 'centimeter', 'millimeter', 'meter']:
                                    if 'centimeter' in g.lower() or g.lower() == 'cm':
                                        unit = 'cm'
                                    elif 'millimeter' in g.lower() or g.lower() == 'mm':
                                        unit = 'mm'
                                    elif 'meter' in g.lower() or g.lower() == 'm':
                                        unit = 'm'
                                    break
                            
                            # If no unit found (pure number), infer from value range
                            if unit is None:
                                # For numbers < 1000, assume cm (common for dimensions)
                                # For numbers >= 1000, assume mm
                                if value < 1000:
                                    unit = 'cm'
                                else:
                                    unit = 'mm'
                            
                            # Convert to mm for consistency
                            if unit == 'm':
                                value_mm = value * 1000
                            elif unit == 'cm':
                                value_mm = value * 10
                            else:
                                value_mm = value
                            
                            # Create unique key to avoid duplicates
                            dim_key = (round(value_mm, 1), unit)
                            if dim_key not in seen_dimensions:
                                seen_dimensions.add(dim_key)
                                dimensions.append({
                                    'value': value,
                                    'value_mm': value_mm,
                                    'unit': unit,
                                    'original_text': original_text,  # Keep original text with Korean characters
                                    'confidence': item['confidence'],
                                    'bbox': item['bbox'],
                                    'full_match': match.group()
                                })
                        except (ValueError, IndexError):
                            continue
        
        # Sort by confidence (highest first)
        dimensions.sort(key=lambda x: x['confidence'], reverse=True)
        
        return dimensions
    
    def visualize_results(self, image_path: str, output_path: str, dimensions=None):
        """
        Enhanced visualization with better labeling
        """
        img = cv2.imread(image_path)
        if img is None:
            return None
        
        # Make a copy for drawing
        vis_img = img.copy()
        
        # Get all text
        extracted_data = self.extract_text(image_path)
        
        # Draw all text detections
        for item in extracted_data:
            bbox = item['bbox']
            text = item['text']
            confidence = item['confidence']
            
            # Draw bounding box (green for high confidence, yellow for medium, red for low)
            pts = np.array(bbox, dtype=np.int32)
            if confidence > 0.7:
                color = (0, 255, 0)  # Green
            elif confidence > 0.5:
                color = (0, 255, 255)  # Yellow
            else:
                color = (0, 0, 255)  # Red
            
            cv2.polylines(vis_img, [pts], True, color, 2)
            
            # Draw text label with background for readability
            x, y = int(bbox[0][0]), int(bbox[0][1])
            label = f"{text} ({confidence:.2f})"
            
            # Get text size for background
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
            )
            
            # Draw background rectangle
            cv2.rectangle(vis_img, 
                         (x, y - text_height - 10), 
                         (x + text_width, y), 
                         (0, 0, 0), -1)
            
            # Draw text
            cv2.putText(vis_img, label, 
                       (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, color, 2)
        
        # Highlight dimensions specifically if provided
        if dimensions:
            for dim in dimensions:
                bbox = dim['bbox']
                pts = np.array(bbox, dtype=np.int32)
                # Draw thicker box for dimensions
                cv2.polylines(vis_img, [pts], True, (255, 0, 255), 3)
                
                # Add dimension label
                x, y = int(bbox[0][0]), int(bbox[0][1])
                dim_label = f"DIM: {dim['value']} {dim['unit']}"
                (text_width, text_height), _ = cv2.getTextSize(
                    dim_label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
                )
                cv2.rectangle(vis_img, 
                             (x, y - text_height - 15), 
                             (x + text_width + 5, y - 5), 
                             (255, 0, 255), -1)
                cv2.putText(vis_img, dim_label, 
                           (x + 2, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.6, (255, 255, 255), 2)
        
        cv2.imwrite(output_path, vis_img)
        return vis_img
