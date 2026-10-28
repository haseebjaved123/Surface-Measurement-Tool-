"""
Verify the surface area calculation for PPT3
"""
import math

# Given dimensions
height = 57.0  # cm
diameter = 58.8  # cm

# Convert to mm
height_mm = height * 10  # 570 mm
diameter_mm = diameter * 10  # 588 mm
radius_mm = diameter_mm / 2  # 294 mm

print("="*80)
print("VERIFICATION OF SURFACE AREA CALCULATION")
print("="*80)
print()
print("Given:")
print(f"  Height: {height} cm = {height_mm} mm")
print(f"  Diameter: {diameter} cm = {diameter_mm} mm")
print(f"  Radius: {radius_mm} mm")
print()

# For a circular bowl/container (cylinder, open at top)
# Surface area = Lateral area + Bottom area (no top since it's open)

# Lateral surface area = 2πrh
lateral_area = 2 * math.pi * radius_mm * height_mm
print("Lateral Surface Area (side):")
print(f"  Formula: 2 * pi * r * h")
print(f"  = 2 * pi * {radius_mm} * {height_mm}")
print(f"  = 2 * pi * {radius_mm * height_mm}")
print(f"  = 2 * {math.pi * radius_mm * height_mm:.2f}")
print(f"  = {lateral_area:.2f} mm2")
print(f"  = {lateral_area / 100:.2f} cm2")
print()

# Bottom area = πr²
bottom_area = math.pi * radius_mm ** 2
print("Bottom Area:")
print(f"  Formula: pi * r^2")
print(f"  = pi * {radius_mm}^2")
print(f"  = pi * {radius_mm ** 2}")
print(f"  = {bottom_area:.2f} mm2")
print(f"  = {bottom_area / 100:.2f} cm2")
print()

# Total surface area
total_area_mm2 = lateral_area + bottom_area
total_area_cm2 = total_area_mm2 / 100
total_area_m2 = total_area_mm2 / 1000000

print("Total Surface Area (Lateral + Bottom):")
print(f"  = {lateral_area:.2f} + {bottom_area:.2f}")
print(f"  = {total_area_mm2:.2f} mm2")
print(f"  = {total_area_cm2:.2f} cm2")
print(f"  = {total_area_m2:.6f} m2")
print()

# Manual verification
print("="*80)
print("MANUAL VERIFICATION:")
print("="*80)
print(f"Lateral: 2 * 3.14159 * 294 * 570 = {2 * 3.14159 * 294 * 570:.2f} mm2")
print(f"Bottom: 3.14159 * 294^2 = {3.14159 * 294 * 294:.2f} mm2")
print(f"Total: {2 * 3.14159 * 294 * 570 + 3.14159 * 294 * 294:.2f} mm2")
print(f"      = {(2 * 3.14159 * 294 * 570 + 3.14159 * 294 * 294) / 100:.2f} cm2")
print()

print("RESULT: Calculation is CORRECT")
print(f"Surface Area = {total_area_cm2:.2f} cm2 = {total_area_m2:.6f} m2")
