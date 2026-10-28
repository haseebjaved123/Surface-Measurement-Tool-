"""
Measurement 2 - Bucket (바스켓통) Surface Area Calculation
Dimensions: Top D=25cm, Height=25cm, Bottom D=17.8cm
"""
import cv2
import numpy as np
import math
import os

print("="*80)
print("MEASUREMENT 2 - BUCKET SURFACE AREA CALCULATION")
print("="*80)
print()

# Known dimensions from image
top_diameter = 25.0  # cm
height = 25.0  # cm
bottom_diameter = 17.8  # cm

print("EQUIPMENT TYPE: BUCKET (Frustum/Truncated Cone)")
print()
print("DIMENSIONS:")
print(f"  Top Diameter: {top_diameter} cm")
print(f"  Height: {height} cm")
print(f"  Bottom Diameter: {bottom_diameter} cm")
print()

# Convert to mm
top_diameter_mm = top_diameter * 10  # 250 mm
height_mm = height * 10  # 250 mm
bottom_diameter_mm = bottom_diameter * 10  # 178 mm
top_radius_mm = top_diameter_mm / 2  # 125 mm
bottom_radius_mm = bottom_diameter_mm / 2  # 89 mm

# Calculate surface area of bucket (frustum with closed bottom)
# Formula: Lateral Area (frustum) + Bottom Area

# Calculate slant height
slant_height_mm = math.sqrt(height_mm ** 2 + (top_radius_mm - bottom_radius_mm) ** 2)

# Lateral surface area (frustum)
lateral_area_mm2 = math.pi * (top_radius_mm + bottom_radius_mm) * slant_height_mm

# Bottom area (closed bucket)
bottom_area_mm2 = math.pi * bottom_radius_mm ** 2

# Total surface area
total_area_mm2 = lateral_area_mm2 + bottom_area_mm2
total_area_cm2 = total_area_mm2 / 100
total_area_m2 = total_area_mm2 / 1000000

print("="*80)
print("SURFACE AREA CALCULATION:")
print("="*80)
print(f"Shape: Bucket (Frustum/Truncated Cone with closed bottom)")
print()
print(f"FORMULA:")
print(f"  Slant Height (s) = sqrt(h^2 + (R - r)^2)")
print(f"  Lateral Surface Area = pi * (R + r) * s")
print(f"  Bottom Area = pi * r^2")
print(f"  Total Surface Area = Lateral Area + Bottom Area")
print()
print(f"Where:")
print(f"  R = Top radius = {top_diameter} cm / 2 = {top_radius_mm} mm")
print(f"  r = Bottom radius = {bottom_diameter} cm / 2 = {bottom_radius_mm} mm")
print(f"  h = Height = {height} cm = {height_mm} mm")
print()
print(f"Calculation:")
print(f"  Slant Height = sqrt({height_mm}^2 + ({top_radius_mm} - {bottom_radius_mm})^2)")
print(f"                = sqrt({height_mm**2} + {((top_radius_mm - bottom_radius_mm)**2):.2f})")
print(f"                = sqrt({(height_mm**2 + (top_radius_mm - bottom_radius_mm)**2):.2f})")
print(f"                = {slant_height_mm:.2f} mm")
print()
print(f"  Lateral Area = pi * ({top_radius_mm} + {bottom_radius_mm}) * {slant_height_mm:.2f}")
print(f"                = pi * {top_radius_mm + bottom_radius_mm} * {slant_height_mm:.2f}")
print(f"                = {lateral_area_mm2:.2f} mm2")
print(f"                = {lateral_area_mm2/100:.2f} cm2")
print()
print(f"  Bottom Area = pi * {bottom_radius_mm}^2")
print(f"              = {bottom_area_mm2:.2f} mm2")
print(f"              = {bottom_area_mm2/100:.2f} cm2")
print()
print(f"  TOTAL SURFACE AREA = {total_area_mm2:.2f} mm2")
print(f"                      = {total_area_cm2:.2f} cm2")
print(f"                      = {total_area_m2:.6f} m2")
print()

# Read image
img_path = "input_images/measurment 2_바스켓통.PNG"
img_array = np.fromfile(img_path, dtype=np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
h, w = img.shape[:2]

# Create annotated image
annotated = img.copy()

# Draw top diameter measurement line (horizontal, at top)
x_left = 50
x_right = w - 50
y_top = 50

cv2.line(annotated, (x_left, y_top), (x_right, y_top), (0, 255, 0), 3)
# Arrows at both ends
arrow_len = 10
cv2.line(annotated, (x_left, y_top), (x_left + arrow_len, y_top - arrow_len), (0, 255, 0), 3)
cv2.line(annotated, (x_left, y_top), (x_left + arrow_len, y_top + arrow_len), (0, 255, 0), 3)
cv2.line(annotated, (x_right, y_top), (x_right - arrow_len, y_top - arrow_len), (0, 255, 0), 3)
cv2.line(annotated, (x_right, y_top), (x_right - arrow_len, y_top + arrow_len), (0, 255, 0), 3)

# Top diameter label
label = f"{top_diameter} cm"
(tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
mid_x = (x_left + x_right) // 2
cv2.rectangle(annotated, (mid_x - tw // 2 - 5, y_top - th - 15), (mid_x + tw // 2 + 5, y_top - 5),
             (255, 255, 255), -1)
cv2.rectangle(annotated, (mid_x - tw // 2 - 5, y_top - th - 15), (mid_x + tw // 2 + 5, y_top - 5),
             (0, 255, 0), 2)
cv2.putText(annotated, label, (mid_x - tw // 2, y_top - 10),
           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

# Draw height measurement line (vertical, on right side)
x_pos = w - 50
y_top_height = 80
y_bottom_height = h - 80

cv2.line(annotated, (x_pos, y_top_height), (x_pos, y_bottom_height), (0, 255, 0), 3)
# Arrows at both ends
cv2.line(annotated, (x_pos, y_top_height), (x_pos - arrow_len, y_top_height + arrow_len), (0, 255, 0), 3)
cv2.line(annotated, (x_pos, y_top_height), (x_pos + arrow_len, y_top_height + arrow_len), (0, 255, 0), 3)
cv2.line(annotated, (x_pos, y_bottom_height), (x_pos - arrow_len, y_bottom_height - arrow_len), (0, 255, 0), 3)
cv2.line(annotated, (x_pos, y_bottom_height), (x_pos + arrow_len, y_bottom_height - arrow_len), (0, 255, 0), 3)

# Height label
label = f"{height} cm"
(tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
mid_y = (y_top_height + y_bottom_height) // 2
cv2.rectangle(annotated, (x_pos + 12, mid_y - th - 5), (x_pos + 12 + tw + 8, mid_y + 5),
             (255, 255, 255), -1)
cv2.rectangle(annotated, (x_pos + 12, mid_y - th - 5), (x_pos + 12 + tw + 8, mid_y + 5),
             (0, 255, 0), 2)
cv2.putText(annotated, label, (x_pos + 16, mid_y),
           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

# Draw bottom diameter measurement line (horizontal, at bottom)
x_left_bottom = 100
x_right_bottom = w - 100
y_bottom = h - 60

cv2.line(annotated, (x_left_bottom, y_bottom), (x_right_bottom, y_bottom), (0, 255, 0), 3)
# Arrows at both ends
cv2.line(annotated, (x_left_bottom, y_bottom), (x_left_bottom + arrow_len, y_bottom - arrow_len), (0, 255, 0), 3)
cv2.line(annotated, (x_left_bottom, y_bottom), (x_left_bottom + arrow_len, y_bottom + arrow_len), (0, 255, 0), 3)
cv2.line(annotated, (x_right_bottom, y_bottom), (x_right_bottom - arrow_len, y_bottom - arrow_len), (0, 255, 0), 3)
cv2.line(annotated, (x_right_bottom, y_bottom), (x_right_bottom - arrow_len, y_bottom + arrow_len), (0, 255, 0), 3)

# Bottom diameter label
label = f"{bottom_diameter} cm"
(tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
mid_x = (x_left_bottom + x_right_bottom) // 2
cv2.rectangle(annotated, (mid_x - tw // 2 - 5, y_bottom + 15), (mid_x + tw // 2 + 5, y_bottom + th + 20),
             (255, 255, 255), -1)
cv2.rectangle(annotated, (mid_x - tw // 2 - 5, y_bottom + 15), (mid_x + tw // 2 + 5, y_bottom + th + 20),
             (0, 255, 0), 2)
cv2.putText(annotated, label, (mid_x - tw // 2, y_bottom + th + 10),
           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

# Draw calculation result box - minimal and clean
box_margin = int(w * 0.08)  # 8% margin from sides
box_height = int(h * 0.08)  # Only 8% of image height - very small
box_y = h - box_height - int(h * 0.02)  # 2% from bottom

# Semi-transparent white background with subtle border
overlay = annotated.copy()
cv2.rectangle(overlay, (box_margin, box_y), (w - box_margin, box_y + box_height),
             (250, 250, 250), -1)
cv2.addWeighted(overlay, 0.85, annotated, 0.15, 0, annotated)
cv2.rectangle(annotated, (box_margin, box_y), (w - box_margin, box_y + box_height),
             (100, 100, 100), 1)  # Thin gray border

# Calculate font sizes - small and clean
font_scale = max(0.35, w / 1000)
font_thickness = 1

# Single line result - only area, compact and centered
result_text = f"Surface Area: {total_area_cm2:.2f} cm2 ({total_area_m2:.4f} m2)"
(tw, th), baseline = cv2.getTextSize(result_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)

# Center the text
text_x = w // 2 - tw // 2
text_y = box_y + (box_height + th) // 2

# Draw text with slight shadow for readability
cv2.putText(annotated, result_text, (text_x + 1, text_y + 1),
           cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), font_thickness + 1)
cv2.putText(annotated, result_text, (text_x, text_y),
           cv2.FONT_HERSHEY_SIMPLEX, font_scale, (50, 50, 50), font_thickness)

# Save annotated image (with measurement lines only, no calculation box)
os.makedirs("output_images", exist_ok=True)
annotated_path = "output_images/measurement2_bucket_annotated.jpg"
cv2.imwrite(annotated_path, annotated)

# Create calculated image (with measurement lines + calculation box)
calculated = annotated.copy()

# Draw calculation result box - minimal and clean
box_margin = int(w * 0.08)  # 8% margin from sides
box_height = int(h * 0.08)  # Only 8% of image height - very small
box_y = h - box_height - int(h * 0.02)  # 2% from bottom

# Semi-transparent white background with subtle border
overlay = calculated.copy()
cv2.rectangle(overlay, (box_margin, box_y), (w - box_margin, box_y + box_height),
             (250, 250, 250), -1)
cv2.addWeighted(overlay, 0.85, calculated, 0.15, 0, calculated)
cv2.rectangle(calculated, (box_margin, box_y), (w - box_margin, box_y + box_height),
             (100, 100, 100), 1)  # Thin gray border

# Calculate font sizes - smaller font
font_scale = max(0.28, w / 1200)  # Reduced
font_thickness = 1

# Single line result - only area, compact and centered
result_text = f"Surface Area: {total_area_cm2:.2f} cm2 ({total_area_m2:.4f} m2)"
(tw, th), baseline = cv2.getTextSize(result_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)

# Center the text
text_x = w // 2 - tw // 2
text_y = box_y + (box_height + th) // 2

# Draw text with slight shadow for readability
cv2.putText(calculated, result_text, (text_x + 1, text_y + 1),
           cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), font_thickness + 1)
cv2.putText(calculated, result_text, (text_x, text_y),
           cv2.FONT_HERSHEY_SIMPLEX, font_scale, (50, 50, 50), font_thickness)

# Save calculated image
calculated_path = "output_images/measurement2_bucket_calculated.jpg"
cv2.imwrite(calculated_path, calculated)

print("="*80)
print("RESULT:")
print("="*80)
print(f"Annotated image saved: {annotated_path}")
print(f"Calculated image saved: {calculated_path}")
print()
print(f"THIS BUCKET SURFACE AREA = {total_area_cm2:.2f} cm2")
print(f"                          = {total_area_m2:.6f} m2")
print()
print("Images show:")
print("  [OK] Annotated image: Green measurement lines only")
print(f"    - Top Diameter: {top_diameter} cm (horizontal line at top)")
print(f"    - Height: {height} cm (vertical line on right)")
print(f"    - Bottom Diameter: {bottom_diameter} cm (horizontal line at bottom)")
print("  [OK] Calculated image: Measurement lines + Calculation box")
print(f"    - Surface Area = {total_area_cm2:.2f} cm2 ({total_area_m2:.4f} m2)")
print()
print("="*80)
print("SUMMARY:")
print("="*80)
print("Equipment Type: BUCKET (Frustum/Truncated Cone)")
print("Formula Used: Lateral Area (pi * (R + r) * s) + Bottom Area (pi * r^2)")
print(f"Dimensions: Top D={top_diameter}cm, H={height}cm, Bottom D={bottom_diameter}cm")
print(f"Total Surface Area: {total_area_cm2:.2f} cm2 = {total_area_m2:.4f} m2")
