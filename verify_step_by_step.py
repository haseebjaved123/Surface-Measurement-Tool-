"""
Verify calculation step by step as shown in the image
"""
import math

print("="*80)
print("STEP-BY-STEP VERIFICATION")
print("="*80)
print()

# Given
diameter = 58.8  # cm
height = 57.0  # cm

print(f"Given: diameter = {diameter} cm, height = {height} cm")
print()

# Step 1: Radius
radius = diameter / 2
print(f"1. Radius:")
print(f"   r = {diameter}/2 = {radius} cm")
print()

# Step 2: Lateral Surface Area
lateral_formula = 2 * math.pi * radius * height
lateral_pi_term = 2 * radius * height
print(f"2. Lateral Surface Area:")
print(f"   2*pi*r*h = 2 * pi * {radius} * {height}")
print(f"            = 2 * pi * {radius * height}")
print(f"            = {lateral_pi_term}*pi")
print(f"        = {lateral_formula:.2f} cm2")
print()

# Step 3: Bottom Area
bottom_formula = math.pi * radius ** 2
bottom_pi_term = radius ** 2
print(f"3. Bottom Area:")
print(f"   pi*r^2 = pi * {radius}^2")
print(f"          = pi * {bottom_pi_term}")
print(f"          = {bottom_pi_term}*pi")
print(f"       = {bottom_formula:.2f} cm2")
print()

# Step 4: Total
total = lateral_formula + bottom_formula
print(f"4. Total Surface Area (lateral + bottom):")
print(f"   {lateral_formula:.2f} + {bottom_formula:.2f}")
print(f"   = {total:.2f} cm2")
print()

print("="*80)
print("VERIFICATION:")
print("="*80)
print(f"Your calculation shows: 13,244.83 cm2")
print(f"My calculation shows:   {total:.2f} cm2")
print()
if abs(total - 13244.83) < 0.1:
    print("RESULT: CALCULATION IS ACCURATE!")
else:
    print("RESULT: There's a small difference, checking...")
    print(f"Difference: {abs(total - 13244.83):.2f} cm2")
