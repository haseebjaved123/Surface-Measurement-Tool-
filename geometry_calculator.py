"""
Geometric calculations for surface area computation
"""
import math
from typing import Dict, List, Optional

class GeometryCalculator:
    def __init__(self):
        pass
    
    def calculate_cylinder_surface_area(self, diameter: float, height: float, 
                                       include_top_bottom: bool = False) -> Dict:
        """
        Calculate surface area of a cylinder
        Units: mm
        """
        radius = diameter / 2
        lateral_area = 2 * math.pi * radius * height
        top_bottom_area = 2 * math.pi * radius ** 2 if include_top_bottom else 0
        total_area = lateral_area + top_bottom_area
        
        return {
            'shape': 'cylinder',
            'lateral_area_mm2': lateral_area,
            'top_bottom_area_mm2': top_bottom_area,
            'total_area_mm2': total_area,
            'total_area_cm2': total_area / 100,
            'total_area_m2': total_area / 1000000,
            'dimensions': {
                'diameter_mm': diameter,
                'height_mm': height,
                'radius_mm': radius
            }
        }
    
    def calculate_rectangular_surface_area(self, length: float, width: float, 
                                          height: float, include_top_bottom: bool = False) -> Dict:
        """
        Calculate surface area of a rectangular container
        Units: mm
        """
        lateral_area = 2 * (length * height + width * height)
        top_bottom_area = 2 * (length * width) if include_top_bottom else 0
        total_area = lateral_area + top_bottom_area
        
        return {
            'shape': 'rectangular',
            'lateral_area_mm2': lateral_area,
            'top_bottom_area_mm2': top_bottom_area,
            'total_area_mm2': total_area,
            'total_area_cm2': total_area / 100,
            'total_area_m2': total_area / 1000000,
            'dimensions': {
                'length_mm': length,
                'width_mm': width,
                'height_mm': height
            }
        }
    
    def calculate_frustum_surface_area(self, top_diameter: float, bottom_diameter: float,
                                      height: float, slant_height: Optional[float] = None) -> Dict:
        """
        Calculate surface area of a frustum (truncated cone)
        Units: mm
        """
        top_radius = top_diameter / 2
        bottom_radius = bottom_diameter / 2
        
        # Calculate slant height if not provided
        if slant_height is None:
            slant_height = math.sqrt(height ** 2 + (top_radius - bottom_radius) ** 2)
        
        # Lateral surface area of frustum
        lateral_area = math.pi * (top_radius + bottom_radius) * slant_height
        
        # Top and bottom areas
        top_area = math.pi * top_radius ** 2
        bottom_area = math.pi * bottom_radius ** 2
        
        total_area = lateral_area + top_area + bottom_area
        
        return {
            'shape': 'frustum',
            'lateral_area_mm2': lateral_area,
            'top_area_mm2': top_area,
            'bottom_area_mm2': bottom_area,
            'total_area_mm2': total_area,
            'total_area_cm2': total_area / 100,
            'total_area_m2': total_area / 1000000,
            'dimensions': {
                'top_diameter_mm': top_diameter,
                'bottom_diameter_mm': bottom_diameter,
                'height_mm': height,
                'slant_height_mm': slant_height
            }
        }
    
    def calculate_bucket_surface_area(self, top_diameter: float, bottom_diameter: float,
                                     height: float) -> Dict:
        """
        Calculate surface area of a bucket (tapered cylinder)
        Units: mm
        """
        top_radius = top_diameter / 2
        bottom_radius = bottom_diameter / 2
        
        # Calculate slant height
        slant_height = math.sqrt(height ** 2 + (top_radius - bottom_radius) ** 2)
        
        # Lateral surface area (frustum)
        lateral_area = math.pi * (top_radius + bottom_radius) * slant_height
        
        # Bottom area (closed bucket)
        bottom_area = math.pi * bottom_radius ** 2
        
        total_area = lateral_area + bottom_area
        
        return {
            'shape': 'bucket',
            'lateral_area_mm2': lateral_area,
            'bottom_area_mm2': bottom_area,
            'total_area_mm2': total_area,
            'total_area_cm2': total_area / 100,
            'total_area_m2': total_area / 1000000,
            'dimensions': {
                'top_diameter_mm': top_diameter,
                'bottom_diameter_mm': bottom_diameter,
                'height_mm': height
            }
        }
    
    def calculate_scoop_surface_area(self, top_diameter: float, bottom_diameter: float,
                                    height: float) -> Dict:
        """
        Calculate surface area of a scoop (similar to bucket but open)
        Units: mm
        """
        top_radius = top_diameter / 2
        bottom_radius = bottom_diameter / 2
        
        # Calculate slant height
        slant_height = math.sqrt(height ** 2 + (top_radius - bottom_radius) ** 2)
        
        # Lateral surface area (frustum)
        lateral_area = math.pi * (top_radius + bottom_radius) * slant_height
        
        # Bottom area (closed scoop)
        bottom_area = math.pi * bottom_radius ** 2
        
        total_area = lateral_area + bottom_area
        
        return {
            'shape': 'scoop',
            'lateral_area_mm2': lateral_area,
            'bottom_area_mm2': bottom_area,
            'total_area_mm2': total_area,
            'total_area_cm2': total_area / 100,
            'total_area_m2': total_area / 1000000,
            'dimensions': {
                'top_diameter_mm': top_diameter,
                'bottom_diameter_mm': bottom_diameter,
                'height_mm': height
            }
        }
    
    def identify_shape_from_dimensions(self, dimensions: List[Dict]) -> Optional[str]:
        """
        Try to identify the shape based on extracted dimensions
        """
        values = [d['value_mm'] for d in dimensions]
        
        if len(values) == 2:
            # Could be cylinder (diameter, height) or bucket/scoop
            return 'cylinder'
        elif len(values) == 3:
            # Could be rectangular or frustum
            if all(v > 0 for v in values):
                return 'rectangular'
        elif len(values) >= 4:
            # Likely frustum or complex shape
            return 'frustum'
        
        return None
