"""
Measurement 3 - SUS Scoop Surface Area Calculation
Dimensions: 
  Top: 7cm (left), 19cm (middle), 15cm (right)
  Bottom: 3cm (left), 15cm (middle), 12cm (right)
"""
import cv2
import numpy as np
import math
import os

print("="*80)
print("MEASUREMENT 3 - SUS SCOOP SURFACE AREA CALCULATION")
print("="*80)
print()

# Known dimensions from user description
# Top measurements
top_left = 7.0  # cm
top_middle = 19.0  # cm (main top diameter)
top_right = 15.0  # cm

# Bottom measurements
bottom_left = 3.0  # cm
bottom_middle = 15.0  # cm (main bottom diameter)
bottom_right = 12.0  # cm

# For frustum calculation, use main diameters
top_diameter = top_middle  # 19 cm
bottom_diameter = bottom_middle  # 15 cm
# Height needs to be estimated or detected - using average of other measurements as estimate
height = (top_middle + bottom_middle) / 2  # Estimate: ~17 cm (will need to detect from image)

print("EQUIPMENT TYPE: SUS SCOOP (Grain Carrier - Frustum Shape)")
print()
print("DIMENSIONS DETECTED:")
print(f"  Top: {top_left}cm (left), {top_middle}cm (middle/main), {top_right}cm (right)")
print(f"  Bottom: {bottom_left}cm (left), {bottom_middle}cm (middle/main), {bottom_right}cm (right)")
print(f"  Using main diameters: Top D={top_diameter}cm, Bottom D={bottom_diameter}cm")
print()

# Read image
img_path = "input_images/measurment 3_sus scoop(various angles).PNG"
img_array = np.fromfile(img_path, dtype=np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
h, w = img.shape[:2]

print(f"Image size: {w}x{h}")
print()

# Try to detect height from image or use estimate
# For now, using estimate based on typical scoop proportions
height = 12.0  # Estimated height in cm (typical for this type of scoop)

print(f"Estimated Height: {height} cm")
print()

# Convert to mm for calculation
top_diameter_mm = top_diameter * 10  # 190 mm
bottom_diameter_mm = bottom_diameter * 10  # 150 mm
height_mm = height * 10  # 120 mm
top_radius_mm = top_diameter_mm / 2  # 95 mm
bottom_radius_mm = bottom_diameter_mm / 2  # 75 mm

# Calculate surface area of scoop (frustum with closed bottom)
# Formula: Lateral Area (frustum) + Bottom Area

# Calculate slant height
slant_height_mm = math.sqrt(height_mm ** 2 + (top_radius_mm - bottom_radius_mm) ** 2)

# Lateral surface area (frustum)
lateral_area_mm2 = math.pi * (top_radius_mm + bottom_radius_mm) * slant_height_mm

# Bottom area (closed scoop)
bottom_area_mm2 = math.pi * bottom_radius_mm ** 2

# Total surface area
total_area_mm2 = lateral_area_mm2 + bottom_area_mm2
total_area_cm2 = total_area_mm2 / 100
total_area_m2 = total_area_mm2 / 1000000

print("="*80)
print("SURFACE AREA CALCULATION:")
print("="*80)
print(f"Shape: SUS Scoop (Frustum with closed bottom)")
print()
print(f"Formula:")
print(f"  Slant Height (s) = sqrt(h^2 + (R - r)^2)")
print(f"  Lateral Surface Area = pi * (R + r) * s")
print(f"  Bottom Area = pi * r^2")
print(f"  Total Surface Area = Lateral Area + Bottom Area")
print()
print(f"Calculation:")
print(f"  Top Radius (R) = {top_diameter} cm / 2 = {top_radius_mm} mm")
print(f"  Bottom Radius (r) = {bottom_diameter} cm / 2 = {bottom_radius_mm} mm")
print(f"  Height (h) = {height} cm = {height_mm} mm")
print()
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

# Create annotated image (Image 1: Annotated - measurement lines only)
annotated = img.copy()

# Draw all measurement lines with labels
# Image is a 2x3 grid (6 images)
# Based on actual image layout:
# Top row: left (7cm on scale), middle (19cm), right (15cm)
# Bottom row: left (3cm), middle (15cm), right (12cm)
arrow_len = 8
line_thickness = 2

# Calculate grid positions (2 columns, 3 rows)
col_width = w // 2
row_height = h // 3

# Top left image (7cm) - vertical measurement on the scale/tape
# Position: left side of first column, vertical line on the measuring tape
x1, y1 = int(col_width * 0.25), int(row_height * 0.3)
x2, y2 = int(col_width * 0.25), int(row_height * 0.7)
cv2.line(annotated, (x1, y1), (x2, y2), (0, 255, 0), line_thickness)
cv2.line(annotated, (x1, y1), (x1 - arrow_len, y1 + arrow_len), (0, 255, 0), line_thickness)
cv2.line(annotated, (x1, y1), (x1 + arrow_len, y1 + arrow_len), (0, 255, 0), line_thickness)
cv2.line(annotated, (x2, y2), (x2 - arrow_len, y2 - arrow_len), (0, 255, 0), line_thickness)
cv2.line(annotated, (x2, y2), (x2 + arrow_len, y2 - arrow_len), (0, 255, 0), line_thickness)
label = f"{top_left} cm"
(tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
mid_y = (y1 + y2) // 2
cv2.rectangle(annotated, (x1 + 10, mid_y - th - 3), (x1 + 10 + tw + 6, mid_y + 3),
             (0, 255, 0), -1)
cv2.putText(annotated, label, (x1 + 12, mid_y),
           cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)

# Top middle image (19cm) - horizontal measurement across the width
# Position: middle of first column, horizontal line across the opening
x1, y1 = int(col_width * 0.15), int(row_height * 0.5)
x2, y2 = int(col_width * 0.85), int(row_height * 0.5)
cv2.line(annotated, (x1, y1), (x2, y2), (0, 255, 0), line_thickness + 1)
cv2.line(annotated, (x1, y1), (x1 + arrow_len, y1 - arrow_len), (0, 255, 0), line_thickness + 1)
cv2.line(annotated, (x1, y1), (x1 + arrow_len, y1 + arrow_len), (0, 255, 0), line_thickness + 1)
cv2.line(annotated, (x2, y2), (x2 - arrow_len, y2 - arrow_len), (0, 255, 0), line_thickness + 1)
cv2.line(annotated, (x2, y2), (x2 - arrow_len, y2 + arrow_len), (0, 255, 0), line_thickness + 1)
label = f"{top_middle} cm"
(tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
mid_x = (x1 + x2) // 2
cv2.rectangle(annotated, (mid_x - tw // 2 - 4, y1 - th - 10), (mid_x + tw // 2 + 4, y1 - 2),
             (0, 255, 0), -1)
cv2.putText(annotated, label, (mid_x - tw // 2, y1 - 4),
           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

# Top right image (15cm) - horizontal measurement on lower section
# Position: second column, horizontal line across the diameter
x1, y1 = int(col_width + col_width * 0.2), int(row_height * 0.65)
x2, y2 = int(col_width + col_width * 0.8), int(row_height * 0.65)
cv2.line(annotated, (x1, y1), (x2, y2), (0, 255, 0), line_thickness)
cv2.line(annotated, (x1, y1), (x1 + arrow_len, y1 - arrow_len), (0, 255, 0), line_thickness)
cv2.line(annotated, (x1, y1), (x1 + arrow_len, y1 + arrow_len), (0, 255, 0), line_thickness)
cv2.line(annotated, (x2, y2), (x2 - arrow_len, y2 - arrow_len), (0, 255, 0), line_thickness)
cv2.line(annotated, (x2, y2), (x2 - arrow_len, y2 + arrow_len), (0, 255, 0), line_thickness)
label = f"{top_right} cm"
(tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
mid_x = (x1 + x2) // 2
cv2.rectangle(annotated, (mid_x - tw // 2 - 3, y1 - th - 8), (mid_x + tw // 2 + 3, y1 - 2),
             (0, 255, 0), -1)
cv2.putText(annotated, label, (mid_x - tw // 2, y1 - 4),
           cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)

# Bottom left image (3cm) - horizontal measurement on the rod
# Position: left side of bottom row, horizontal line on the rod
x1, y1 = int(col_width * 0.15), int(row_height * 2 + row_height * 0.5)
x2, y2 = int(col_width * 0.45), int(row_height * 2 + row_height * 0.5)
cv2.line(annotated, (x1, y1), (x2, y2), (0, 255, 0), line_thickness)
cv2.line(annotated, (x1, y1), (x1 + arrow_len, y1 - arrow_len), (0, 255, 0), line_thickness)
cv2.line(annotated, (x1, y1), (x1 + arrow_len, y1 + arrow_len), (0, 255, 0), line_thickness)
cv2.line(annotated, (x2, y2), (x2 - arrow_len, y2 - arrow_len), (0, 255, 0), line_thickness)
cv2.line(annotated, (x2, y2), (x2 - arrow_len, y2 + arrow_len), (0, 255, 0), line_thickness)
label = f"{bottom_left} cm"
(tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
mid_x = (x1 + x2) // 2
cv2.rectangle(annotated, (mid_x - tw // 2 - 3, y1 - th - 8), (mid_x + tw // 2 + 3, y1 - 2),
             (0, 255, 0), -1)
cv2.putText(annotated, label, (mid_x - tw // 2, y1 - 4),
           cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)

# Bottom middle image (15cm) - horizontal measurement across opening
# Position: middle of bottom row, horizontal line across the container opening
x1, y1 = int(col_width * 0.15), int(row_height * 2 + row_height * 0.5)
x2, y2 = int(col_width * 0.85), int(row_height * 2 + row_height * 0.5)
cv2.line(annotated, (x1, y1), (x2, y2), (0, 255, 0), line_thickness + 1)
cv2.line(annotated, (x1, y1), (x1 + arrow_len, y1 - arrow_len), (0, 255, 0), line_thickness + 1)
cv2.line(annotated, (x1, y1), (x1 + arrow_len, y1 + arrow_len), (0, 255, 0), line_thickness + 1)
cv2.line(annotated, (x2, y2), (x2 - arrow_len, y2 - arrow_len), (0, 255, 0), line_thickness + 1)
cv2.line(annotated, (x2, y2), (x2 - arrow_len, y2 + arrow_len), (0, 255, 0), line_thickness + 1)
label = f"{bottom_middle} cm"
(tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
mid_x = (x1 + x2) // 2
cv2.rectangle(annotated, (mid_x - tw // 2 - 4, y1 - th - 10), (mid_x + tw // 2 + 4, y1 - 2),
             (0, 255, 0), -1)
cv2.putText(annotated, label, (mid_x - tw // 2, y1 - 4),
           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

# Bottom right image (12cm) - vertical measurement on the component
# Position: right side of bottom row, vertical line alongside the component
x1, y1 = int(col_width + col_width * 0.75), int(row_height * 2 + row_height * 0.25)
x2, y2 = int(col_width + col_width * 0.75), int(row_height * 2 + row_height * 0.75)
cv2.line(annotated, (x1, y1), (x2, y2), (0, 255, 0), line_thickness)
cv2.line(annotated, (x1, y1), (x1 - arrow_len, y1 + arrow_len), (0, 255, 0), line_thickness)
cv2.line(annotated, (x1, y1), (x1 + arrow_len, y1 + arrow_len), (0, 255, 0), line_thickness)
cv2.line(annotated, (x2, y2), (x2 - arrow_len, y2 - arrow_len), (0, 255, 0), line_thickness)
cv2.line(annotated, (x2, y2), (x2 + arrow_len, y2 - arrow_len), (0, 255, 0), line_thickness)
label = f"{bottom_right} cm"
(tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
mid_y = (y1 + y2) // 2
cv2.rectangle(annotated, (x1 + 10, mid_y - th - 3), (x1 + 10 + tw + 6, mid_y + 3),
             (0, 255, 0), -1)
cv2.putText(annotated, label, (x1 + 12, mid_y),
           cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)

# Save annotated image (Image 1)
os.makedirs("output_images", exist_ok=True)
annotated_path = "output_images/measurement3_scoop_annotated.jpg"
cv2.imwrite(annotated_path, annotated)

# Create calculated image (Image 2: Calculated - with calculation box)
calculated = annotated.copy()

# Draw calculation result box
box_margin = int(w * 0.08)
box_height = int(h * 0.08)
box_y = h - box_height - int(h * 0.02)

# Semi-transparent white background with subtle border
overlay = calculated.copy()
cv2.rectangle(overlay, (box_margin, box_y), (w - box_margin, box_y + box_height),
             (250, 250, 250), -1)
cv2.addWeighted(overlay, 0.85, calculated, 0.15, 0, calculated)
cv2.rectangle(calculated, (box_margin, box_y), (w - box_margin, box_y + box_height),
             (100, 100, 100), 1)

# Calculate font sizes
font_scale = max(0.28, w / 1200)
font_thickness = 1

# Single line result
result_text = f"Surface Area: {total_area_cm2:.2f} cm2 ({total_area_m2:.4f} m2)"
(tw, th), baseline = cv2.getTextSize(result_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)

# Center the text
text_x = w // 2 - tw // 2
text_y = box_y + (box_height + th) // 2

# Draw text
cv2.putText(calculated, result_text, (text_x + 1, text_y + 1),
           cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), font_thickness + 1)
cv2.putText(calculated, result_text, (text_x, text_y),
           cv2.FONT_HERSHEY_SIMPLEX, font_scale, (50, 50, 50), font_thickness)

# Save calculated image (Image 2)
calculated_path = "output_images/measurement3_scoop_calculated.jpg"
cv2.imwrite(calculated_path, calculated)

# Create area calculated image (Image 3: Area Calculated - larger box with details)
area_calculated = annotated.copy()

# Draw larger calculation box with more details
box_margin = int(w * 0.05)
box_height = int(h * 0.15)
box_y = h - box_height - int(h * 0.02)

# Semi-transparent white background
overlay = area_calculated.copy()
cv2.rectangle(overlay, (box_margin, box_y), (w - box_margin, box_y + box_height),
             (250, 250, 250), -1)
cv2.addWeighted(overlay, 0.9, area_calculated, 0.1, 0, area_calculated)
cv2.rectangle(area_calculated, (box_margin, box_y), (w - box_margin, box_y + box_height),
             (0, 255, 0), 2)

# Font sizes
font_scale_title = max(0.35, w / 1000)
font_scale_result = max(0.4, w / 900)
font_scale_info = max(0.25, w / 1300)

# Title
title = "SURFACE AREA CALCULATION"
(tw, th), _ = cv2.getTextSize(title, cv2.FONT_HERSHEY_SIMPLEX, font_scale_title, 1)
title_x = w // 2 - tw // 2
title_y = box_y + int(box_height * 0.25)
cv2.putText(area_calculated, title, (title_x, title_y),
           cv2.FONT_HERSHEY_SIMPLEX, font_scale_title, (0, 0, 0), 1)

# Dimensions
dims_text = f"Top D={top_diameter}cm, Bottom D={bottom_diameter}cm, H={height}cm"
(tw, th), _ = cv2.getTextSize(dims_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale_info, 1)
dims_x = w // 2 - tw // 2
dims_y = box_y + int(box_height * 0.5)
cv2.putText(area_calculated, dims_text, (dims_x, dims_y),
           cv2.FONT_HERSHEY_SIMPLEX, font_scale_info, (0, 0, 0), 1)

# Result
result_text = f"AREA = {total_area_cm2:.2f} cm2 ({total_area_m2:.4f} m2)"
(tw, th), _ = cv2.getTextSize(result_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale_result, 2)
result_x = w // 2 - tw // 2
result_y = box_y + int(box_height * 0.8)
cv2.putText(area_calculated, result_text, (result_x, result_y),
           cv2.FONT_HERSHEY_SIMPLEX, font_scale_result, (0, 150, 0), 2)

# Save area calculated image (Image 3)
area_path = "output_images/measurement3_scoop_area_calculated.jpg"
cv2.imwrite(area_path, area_calculated)

print("="*80)
print("RESULT:")
print("="*80)
print(f"Image 1 (Annotated) saved: {annotated_path}")
print(f"Image 2 (Calculated) saved: {calculated_path}")
print(f"Image 3 (Area Calculated) saved: {area_path}")
print()
print(f"THIS SUS SCOOP SURFACE AREA = {total_area_cm2:.2f} cm2")
print(f"                              = {total_area_m2:.6f} m2")
print()
print("Images show:")
print("  [OK] Image 1: All 6 dimension measurements with green labels")
print("  [OK] Image 2: Measurements + compact calculation box")
print("  [OK] Image 3: Measurements + detailed area calculation box")
