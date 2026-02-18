"""
Smart equipment identification and surface area calculation
"""
import math
from typing import Dict, List, Optional

class SmartCalculator:
    def __init__(self):
        pass
    
    def identify_equipment_type(self, dimensions: List[Dict], image_name: str = "") -> str:
        """
        Smart identification of equipment type based on dimensions and filename
        """
        values_mm = [d['value_mm'] for d in dimensions]
        num_dims = len(dimensions)
        
        # Check filename for hints
        name_lower = image_name.lower()
        
        # Scoop detection
        if 'scoop' in name_lower or num_dims == 3:
            if num_dims >= 3:
                # Top, bottom, height
                return 'scoop'
        
        # Bucket detection
        if 'bucket' in name_lower or '통' in name_lower or '바스켓' in name_lower:
            if num_dims >= 3:
                return 'bucket'
        
        # Hopper detection
        if 'hopper' in name_lower or '호퍼' in name_lower:
            if num_dims >= 4:
                return 'hopper'
            return 'frustum'
        
        # Tank/Container detection
        if 'tank' in name_lower or '탱크' in name_lower or 'container' in name_lower:
            if num_dims == 2:
                return 'cylinder'
            elif num_dims == 3:
                # Check if rectangular or cylindrical
                if abs(values_mm[0] - values_mm[1]) < values_mm[0] * 0.1:
                    return 'cylinder'  # Similar length/width = cylinder
                return 'rectangular'
        
        # Mixer detection
        if 'mixer' in name_lower or '혼합' in name_lower:
            if num_dims >= 3:
                return 'frustum'
        
        # Default logic based on dimension count
        if num_dims == 2:
            # Likely cylinder (diameter, height)
            if values_mm[0] > values_mm[1] * 0.5:  # Diameter reasonable
                return 'cylinder'
        elif num_dims == 3:
            # Could be rectangular or frustum
            # If two similar values, likely rectangular
            if abs(values_mm[0] - values_mm[1]) < max(values_mm) * 0.2:
                return 'rectangular'
            else:
                # Likely frustum/bucket/scoop
                return 'frustum'
        elif num_dims >= 4:
            return 'frustum'  # Complex shape
        
        return 'unknown'
    
    def calculate_smart(self, dimensions: List[Dict], image_name: str = "") -> Dict:
        """
        Smart calculation based on identified equipment type
        """
        if len(dimensions) < 2:
            return None
        
        values_mm = [d['value_mm'] for d in dimensions]
        eq_type = self.identify_equipment_type(dimensions, image_name)
        
        from geometry_calculator import GeometryCalculator
        calc = GeometryCalculator()
        
        if eq_type == 'cylinder':
            diameter = max(values_mm[0], values_mm[1])
            height = min(values_mm[0], values_mm[1])
            return calc.calculate_cylinder_surface_area(diameter, height, include_top_bottom=False)
        
        elif eq_type == 'rectangular':
            length, width, height = values_mm[0], values_mm[1], values_mm[2]
            return calc.calculate_rectangular_surface_area(length, width, height, include_top_bottom=False)
        
        elif eq_type in ['scoop', 'bucket']:
            if len(values_mm) >= 3:
                top_d = max(values_mm[0], values_mm[1])
                bottom_d = min(values_mm[0], values_mm[1])
                height = values_mm[2] if len(values_mm) > 2 else values_mm[1]
                if eq_type == 'scoop':
                    return calc.calculate_scoop_surface_area(top_d, bottom_d, height)
                else:
                    return calc.calculate_bucket_surface_area(top_d, bottom_d, height)
        
        elif eq_type in ['frustum', 'hopper']:
            if len(values_mm) >= 3:
                top_d = values_mm[0]
                bottom_d = values_mm[1] if len(values_mm) > 1 else values_mm[0] * 0.3
                height = values_mm[2] if len(values_mm) > 2 else values_mm[1]
                slant = values_mm[3] if len(values_mm) > 3 else None
                return calc.calculate_frustum_surface_area(top_d, bottom_d, height, slant)
        
        return None
