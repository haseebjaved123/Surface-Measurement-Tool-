"""Quick test to verify everything is installed correctly"""
import os
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'

try:
    print("Testing imports...")
    from main import IndustrialToolAnalyzer
    print("[OK] All imports successful!")
    print("[OK] System is ready to use!")
    print()
    print("Next step: Add images to 'input_images' folder and run simple_run.py")
except Exception as e:
    print(f"[ERROR] {e}")
    print("Please install dependencies: pip install -r requirements.txt")
