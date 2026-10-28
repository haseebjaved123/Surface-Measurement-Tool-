"""
Download sample industrial tool images for testing
"""
import os
import requests
from pathlib import Path

input_dir = "input_images"
os.makedirs(input_dir, exist_ok=True)

# Sample URLs for industrial tool images with dimensions
# These are placeholder - in real scenario, user would provide their images
print("="*80)
print("INDUSTRIAL TOOL IMAGE DOWNLOADER")
print("="*80)
print()
print("NOTE: You need to add your industrial tool images to the 'input_images' folder.")
print()
print("The images you described:")
print("  1. Blue plastic scoop (19cm top, 14cm bottom, 11cm height)")
print("  2. Blue plastic bucket (25cm top, 17.8cm bottom, 25cm height)")
print("  3. White spatula (22.5cm length, 9cm wide)")
print("  4. Polished metal object with measurements")
print("  5. Rectangular stainless steel container (330mm x 270mm x 150mm)")
print("  6. Textured surface (305mm x 250mm)")
print("  7. Metallic bucket (57cm height, 58.8cm diameter)")
print("  8. Stainless steel equipment (4 views)")
print("  9. Hopper technical drawing")
print()
print("Please copy these images to: input_images/ folder")
print("Then run: python build_tool.py")
print()
