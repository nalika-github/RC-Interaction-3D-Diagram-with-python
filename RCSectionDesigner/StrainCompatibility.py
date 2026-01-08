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
        # fc is a pint Quantity, extract magnitude in MPa
        fc_MPa_value = fc.to('MPa').magnitude
    else:
        print("Invalid input: fc does not have units. Please ensure fc is a pint Quantity with MPa unit.")
        return None
    
    print(f'fc = {fc_MPa_value} MPa')
    
    # Calculate beta1 according to ACI 318
    if fc_MPa_value <= 28:
        return 0.85
    elif fc_MPa_value <= 55:
        return max(0.85 - 0.05 * (fc_MPa_value - 28) / 7, 0.65)
    else:
        return 0.65

class StrainCompatibility:
    def __init__ (self, section_data, neutral_axis_y = 0):
        self.section_data = section_data
        self.beta1 = beta1(section_data.concrete_material_properties)
        self.neutral_axis_y = neutral_axis_y
        self.topconfiber = np.max(section_data.ro_polygon.exterior.xy[1])
        self.bottomconfiber = np.min(section_data.ro_polygon.exterior.xy[1])
        self.toprebarfiber = np.max([coord.y for coord in section_data.ro_rebarCoor.geoms])
        self.bottomrebarfiber = np.min([coord.y for coord in section_data.ro_rebarCoor.geoms])
        self.cut_y = self.topconfiber - (self.topconfiber - self.neutral_axis_y) * self.beta1
        self.compression_polygon = sectionCut(section_data, self.cut_y)
        # self.strainline = cal_strainline(cut_y, section_data.concrete_compressive_strain, section_data.length_unit)
        self.concrete_compressive_strain = 0.003  # Typical value for concrete
        self.compression_force = self.cal_conrete_compresive_force(section_data)
        self.compression_rebar = self.get_compression_rebar(section_data)  # Placeholder for compression rebar data
        self.tension_rebar = self.get_tension_rebar(section_data)  # Placeholder for tension rebar data
        self.rebar_force = self.cal_rebar_force(section_data)
        self.length_unit = section_data.length_unit
        # print("Compression Polygon:", self.compression_polygon)
        # print("compression_rebar",self.compression_rebar)

    def cal_conrete_compresive_force(self, section_data):
        area_unit = section_data.length_unit**2
        area = Q_(self.compression_polygon.area, area_unit)
        fc = section_data.concrete_material_properties
        Pn = area * fc
        Pn = Pn.to('kN')  # Convert force to kN
        return Pn

    def cal_rebar_force(self, section_data):
        rebar_force = []
        slope = self.concrete_compressive_strain / (self.topconfiber - self.neutral_axis_y)
        Es = section_data.Es # Young's modulus for steel

        for idx, coord in enumerate(section_data.ro_rebarCoor.geoms):
            # Calculate strain
            rebar_strain = self.concrete_compressive_strain - (slope * (self.topconfiber - coord.y))
            
            # Get material properties
            rebar_key = 'R' + str(idx)
            fy = section_data.rebars_material_properties[rebar_key]['fy']
            rebar_area = section_data.rebars_material_properties[rebar_key]['Area']
            
            # Calculate stress (with yield check)
            if abs(rebar_strain * Es) <= fy:
                stress = rebar_strain * Es  # Elastic range
            else:
                stress = fy if rebar_strain > 0 else -fy  # Yielded
            
            # Calculate area and force: F = stress × area
            force = stress * rebar_area
            force = force.to('kN')  # Convert force to kN
            
            rebar_force.append(force)
        print ("rebar force: \n", rebar_force)
        return rebar_force

    def PM_Point(self):
        # Calculate total axial force (compression positive)
        print("Rebar Forces:", self.rebar_force)
        print("Concrete Compression Force:", self.compression_force)
        P_n = 0
        for force in self.rebar_force:
            P_n += force
        P_n += self.compression_force
        print("Total Axial Force P_n:", P_n)
        
        # Calculate moment contribution from concrete compression
        centroid = self.compression_polygon.centroid
        concrete_moment_arm = Q_(self.topconfiber - centroid.y, self.length_unit)
        M_concrete = self.compression_force * concrete_moment_arm
        print("Concrete Moment M_concrete:", M_concrete)
        
        # Calculate moment contribution from all rebars
        M_rebar = 0
        for index, force in enumerate(self.rebar_force):
            coord = self.section_data.ro_rebarCoor.geoms[index]
            rebar_moment_arm = Q_(self.topconfiber - coord.y, self.length_unit)
            M_rebar += force * rebar_moment_arm

        M_n = M_concrete + M_rebar
        M_n = M_n.to('kN*m')  # Convert moment to kN*m
        print("Total Moment M_n:", M_n)
        return {'P_n': P_n, 'M_n': M_n}

    def plot_PMM(self):
        PMM = self.PM_Point()
        fig, ax = plt.subplots()
        ax.plot(PMM['M_n'].magnitude, PMM['P_n'].magnitude, 'bo')
        ax.set_xlabel(f'Moment (kN·m)')
        ax.set_ylabel(f'Axial Force (kN)')
        ax.set_title('P-M Interaction Point')
        plt.grid()
        plt.show()

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
        patch_concrete = patch_from_polygon(self.compression_polygon, facecolor='gray', edgecolor='black')
        compression_rebar_x = [coord[0] for coord in self.compression_rebar.values()]
        compression_rebar_y = [coord[1] for coord in self.compression_rebar.values()]
        tension_rebar_x = [coord[0] for coord in self.tension_rebar.values()]
        tension_rebar_y = [coord[1] for coord in self.tension_rebar.values()]
        ax.scatter(compression_rebar_x, compression_rebar_y, color='red', label='Compression Rebar', zorder=5)
        ax.scatter(tension_rebar_x, tension_rebar_y, color='blue', label='Tension Rebar', zorder=5)
        ax.add_patch(patch_concrete)

        # Get bounds from actual coordinates
        # Collect all coordinates from polygon and rebars
        all_coords = list(self.compression_polygon.exterior.coords)
        all_coords.extend(self.compression_rebar.values())
        all_coords.extend(self.tension_rebar.values())
        
        min_x, min_y = np.min(all_coords, axis=0)
        max_x, max_y = np.max(all_coords, axis=0)
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