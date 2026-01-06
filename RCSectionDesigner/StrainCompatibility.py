from shapely.geometry import Polygon, LineString, MultiPolygon
from shapely.affinity import translate
from shapely.plotting import patch_from_polygon
import matplotlib.pyplot as plt
import numpy as np

from RCSectionDesigner.units import Q_

def sectionCut(section_data, cut_y):
    x = section_data.ro_polygon.exterior.xy[0]
    y = section_data.ro_polygon.exterior.xy[1]
    cutting_line = LineString([(min(x),cut_y),(max(x),cut_y)])

    full_section = section_data.ro_polygon
    # for poly in full_section.geoms:
    #     x,y = poly.exterior.xy
    #     plt.fill(x, y, alpha=0.5, fc='lightgrey', ec='black')
    
    # วาดเส้น LineString ในกราฟเดียวกัน
    cut_x, cut_y = cutting_line.xy
    # plt.plot(cut_x, cut_y, color='red', linestyle='--', linewidth=2, label='Cut Line')
    
    # คำนวณ buffer distance จาก bounds ของ section
    buffer_distance = max(y) - min(cut_y)  # ระยะจากเส้นตัดถึงขอบบนสุด
    compression_zone = cutting_line.buffer(buffer_distance, single_sided=True)

    cut_part = full_section.intersection(compression_zone)
    return cut_part

def beta1(fc):
    # Check if fc has pint unit
    if hasattr(fc, 'units'):
        # fc is a pint Quantity, extract magnitude
        fc_MPa = fc.to('MPa')
    else:
        print("Invalide input: fc does not have units. Please ensure fc is a pint Quantity with MPa unit.")
        return None
        
    # Calculate beta1 according to ACI 318
    if fc_MPa <= Q_(28, 'MPa'):
        return 0.85
    elif fc_MPa <= Q_(55, 'MPa'):
        return max(0.85 - 0.05 * (fc_MPa - Q_(28, 'MPa')) / Q_(7, 'MPa'), 0.65)
    else:
        return 0.65
    pass


class StrainCompatibility:
    def __init__ (self, section_data, cut_y):
        self.compression_polygon = sectionCut(section_data, cut_y)
        self.cut_y = cut_y 
        # self.strainline = cal_strainline(cut_y, section_data.concrete_compressive_strain, section_data.length_unit)
        self.bata1 = None  # Placeholder for strain at extreme compression fiber
        self.concrete_compressive_strain = 0.003  # Typical value for concrete
        self.compression_rebar = self.get_compression_rebar(section_data)  # Placeholder for compression rebar data
        self.tension_rebar = self.get_tension_rebar(section_data)  # Placeholder for tension rebar data
        self.length_unit = section_data.length_unit
        self.force_unit = section_data.force_unit

    def PM_Point(self):
        P_n = 0
        M_n = 0
        return {'P_n': P_n, 'M_n': M_n}

    def get_compression_rebar(self, section_data):
        compression_rebar = {}
        for idx, coord in enumerate(section_data.ro_rebarCoor.geoms):
            if coord.y > self.cut_y:
                compression_rebar[idx] = (coord.x, coord.y)
        return compression_rebar
    
    def get_tension_rebar(self, section_data):
        tension_rebar = {}
        for idx, coord in enumerate(section_data.ro_rebarCoor.geoms):
            if coord.y < self.cut_y:
                tension_rebar[idx] = (coord.x, coord.y)
        return tension_rebar

    def plot(self):
        fig, ax = plt.subplots(figsize=(10, 8))
        patch_concrete = patch_from_polygon(self.compression_polygon, facecolor='lightblue', edgecolor='black')
        ax.add_patch(patch_concrete)

        # Get bounds from actual coordinates
        min_x, min_y = np.min(self.compression_polygon.exterior.coords, axis=0)
        max_x, max_y = np.max(self.compression_polygon.exterior.coords, axis=0)
        width = max_x - min_x
        height = max_y - min_y

        # Set axis limits with padding to show entire section
        padding = max(width, height) * 0.1  # 10% padding
        ax.set_xlim(min_x - padding, max_x + padding)
        ax.set_ylim(min_y - padding, max_y + padding)

        # Add origin lines (x=0, y=0)
        ax.axhline(y=0, color='blue', linestyle='--', linewidth=0.5, alpha=0.5, label='y=0')
        ax.axvline(x=0, color='blue', linestyle='--', linewidth=0.5, alpha=0.5, label='x=0')

        ax.set_aspect('equal', 'box')
        plt.title(f'Section Cut at y={self.cut_y} {self.length_unit}')
        plt.xlabel(f'Length ({self.length_unit})')
        plt.ylabel(f'Length ({self.length_unit})')
        plt.grid(True)
        plt.show()
        plt.close(fig)