import pandas as pd
import sys
import numpy as np
from . import config
from .units import ureg, Q_
from shapely.geometry import Polygon, MultiPoint, MultiPolygon, LineString
from shapely import affinity
from shapely.plotting import patch_from_polygon
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


# Functions for importing data (outside class)
def import_coordinates(filepath):
    """
    Import coordinate data from CSV file.
    
    Args:
        filepath: Path to the coordinate CSV file
        
    Returns:
        DataFrame with coordinates
    """
    if(filepath is None):
        print("No filepath provided, please provide a valid path")
    df = pd.read_csv(filepath)
    return df


def prepare_data(rebar_filepath=config.REBAR_COORDINATE_FILE, section_filepath=config.SECTION_COORDINATE_FILE):
    """
    Import and prepare both rebar and section coordinate data.
    
    Args:
        rebar_filepath: Path to the rebar coordinate CSV file (default: from config)
        section_filepath: Path to the section coordinate CSV file (default: from config)
    
    Returns:
        SectionData object containing both dataframes
    """
    rebar_data = import_coordinates(rebar_filepath)
    section_data = import_coordinates(section_filepath)
    
    # Clean data: remove NaN values
    rebar_data = rebar_data.dropna()
    section_data = section_data.dropna()
    
    return SectionData(rebar_data, section_data)


# Class for managing section data
class SectionData:
    """
    Class to manage reinforced concrete section data.
    """
    def __init__(self, 
                 con_matprop,
                 rebar_filepath = config.REBAR_COORDINATE_FILE, 
                 section_filepath = config.SECTION_COORDINATE_FILE, 
                 grade_mapping_filepath = config.REBAR_GRADE_FILE,
                 length_unit="mm", 
                 force_unit="kN"):
        """
        Initialize SectionData with rebar and section dataframes.
        
        Args:
            rebar_df: DataFrame with rebar coordinates (columns: RebarID, X, Y, Diameter, Grade)
            section_df: DataFrame with section coordinates (columns: point, x, y)
        """
        self.length_unit = ureg(length_unit)
        self.force_unit = ureg(force_unit)
        rebar_df = pd.read_csv(rebar_filepath)
        section_df = pd.read_csv(section_filepath)
        rebar_df = rebar_df.dropna()
        section_df = section_df.dropna()
        self.sectionRebarGrade = rebar_df['Grade']
        self.rebarCoor = MultiPoint(rebar_df[['X', 'Y']].to_numpy())
        self.ro_rebarCoor = MultiPoint(section_df[['X', 'Y']].to_numpy())
        self.polygon = Polygon(section_df[['X', 'Y']].to_numpy())
        self.ro_polygon = Polygon(section_df[['X', 'Y']].to_numpy())
        self.concrete_material_properties = con_matprop * self.force_unit/(self.length_unit**2)
        self.rebars_material_properties = self.SetRebarMaterialProperties(grade_mapping_filepath, self.sectionRebarGrade)


    def set_units(self, length_unit="mm", force_unit="kN"):
        """
        Set the units for length and force.
        
        Args:
            length_unit: Length unit (default: "mm")
            force_unit: Force unit (default: "kN")
        """
        self.length_unit = ureg(length_unit)
        self.force_unit = ureg(force_unit)

    def display_info(self):
        """
        Display section and rebar information.
        """
        print("Length Unit:", self.length_unit)

        print(f"Section Coordinates ({self.length_unit}):")
        for coord in self.polygon.exterior.coords:
            print(f"X: {coord[0]}, Y: {coord[1]}")

        print(f"rotated Section Coordinates ({self.length_unit}):")
        for coord in self.ro_polygon.exterior.coords:
            print(f"X: {coord[0]}, Y: {coord[1]}")
        
        print(f"\nRebar Coordinates ({self.length_unit}):")
        for index, point in enumerate(self.rebarCoor.geoms):
            coord = point.coords[0]  # Each Point has one coordinate
            print(f"Tage: R{str(index)} X: {coord[0]}, Y: {coord[1]}")
        
        print("\nConcrete Material Properties:", self.concrete_material_properties)
        print("Rebar Material Properties:", self.rebars_material_properties)

    def SetRebarMaterialProperties(self, grade_mapping_filepath, sectionRebarGrade):
        rebarGrade_df = pd.read_csv(grade_mapping_filepath).dropna()
        rebar_matprop = {}

        for i, grade in sectionRebarGrade.items():
            fy = rebarGrade_df.loc[rebarGrade_df['Grade'] == grade, 'Yield_Strength_MPa'].values
            fy = Q_(fy[0], 'MPa')
            fu = rebarGrade_df.loc[rebarGrade_df['Grade'] == grade, 'Tensile_Strength_MPa'].values
            fu = Q_(fu[0], 'MPa')
            rebar_matprop['R' + str(i)] = {'fy': fy, 'fu': fu}

        return rebar_matprop

        # for index, row in rebarGrade_df.iterrows():
        #     print(row)
        #     print("-------------------")
        #     print(sectionRebarGrade)
        #     print("-------------------")
            

    def rotate_section(self, angle_degrees = 0, origin='center'):
        """
        Rotate the section polygon and rebar coordinates by a given angle.
        
        Args:
            angle_degrees: Angle to rotate in degrees
            origin: Point around which to rotate (default: 'center')
        """
        self.ro_polygon = affinity.rotate(self.polygon, angle_degrees, origin=origin)
        self.ro_rebarCoor = affinity.rotate(self.rebarCoor, angle_degrees, origin=origin)


    def plot(self, is_rotated = False):
        """
        Plot the reinforced concrete section using the plotRCSection module.
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        if is_rotated:
            patch_concrete = patch_from_polygon(self.ro_polygon, facecolor='grey', edgecolor='black')
        else:
            patch_concrete = patch_from_polygon(self.polygon, facecolor='grey', edgecolor='black')
        ax.add_patch(patch_concrete)

        # Get bounds from actual coordinates
        if is_rotated:
            min_x, min_y = np.min(self.ro_polygon.exterior.coords, axis=0)
            max_x, max_y = np.max(self.ro_polygon.exterior.coords, axis=0)
        else:
            min_x, min_y = np.min(self.polygon.exterior.coords, axis=0)
            max_x, max_y = np.max(self.polygon.exterior.coords, axis=0)
        width = max_x - min_x
        height = max_y - min_y
        
        # Calculate appropriate rebar radius (based on section size)
        rebar_radius = min(width, height) * 0.02  # 2% of smaller dimension
        
        # Plot rebar positions
        if is_rotated:
            for coord in self.ro_rebarCoor.geoms:
                rebar_patch = Circle((coord.x, coord.y), radius=rebar_radius, color='red', alpha=0.8)
                ax.add_patch(rebar_patch)
        else:
            for coord in self.rebarCoor.geoms:
                rebar_patch = Circle((coord.x, coord.y), radius=rebar_radius, color='red', alpha=0.8)
                ax.add_patch(rebar_patch)
        
        # Set axis limits with padding to show entire section
        padding = max(width, height) * 0.1  # 10% padding
        ax.set_xlim(min_x - padding, max_x + padding)
        ax.set_ylim(min_y - padding, max_y + padding)
        
        # Add origin lines (x=0, y=0)
        ax.axhline(y=0, color='blue', linestyle='--', linewidth=0.5, alpha=0.5, label='y=0')
        ax.axvline(x=0, color='blue', linestyle='--', linewidth=0.5, alpha=0.5, label='x=0')
        
        ax.set_aspect('equal', 'box')
        ax.set_xlabel('X Coordinate (m)', fontsize=12)
        ax.set_ylabel('Y Coordinate (m)', fontsize=12)
        ax.set_title('Reinforced Concrete Section', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        plt.tight_layout()
        plt.show()
        plt.close(fig)