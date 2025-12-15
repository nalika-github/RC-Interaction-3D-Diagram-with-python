from queue import Full
import pandas as pd
import numpy as np
from . import config
from .units import ureg, Q_


# Functions for importing data (outside class)
def import_rebar_coordinates(filepath=None):
    """
    Import rebar coordinate data from CSV file.
    
    Args:
        filepath: Path to the rebar coordinate CSV file (default: from config)
        
    Returns:
        DataFrame with rebar coordinates
    """
    if filepath is None:
        filepath = config.REBAR_COORDINATE_FILE
    df = pd.read_csv(filepath)
    return df


def import_section_coordinates(filepath=None):
    """
    Import section coordinate data from CSV file.
    
    Args:
        filepath: Path to the section coordinate CSV file (default: from config)
        
    Returns:
        DataFrame with section coordinates
    """
    if filepath is None:
        filepath = config.SECTION_COORDINATE_FILE
    df = pd.read_csv(filepath)
    return df


def prepare_data(rebar_filepath=None, section_filepath=None):
    """
    Import and prepare both rebar and section coordinate data.
    
    Args:
        rebar_filepath: Path to the rebar coordinate CSV file (default: from config)
        section_filepath: Path to the section coordinate CSV file (default: from config)
        
    Returns:
        SectionData object containing both dataframes
    """
    rebar_data = import_rebar_coordinates(rebar_filepath)
    section_data = import_section_coordinates(section_filepath)
    
    # Clean data: remove NaN values
    rebar_data = rebar_data.dropna()
    section_data = section_data.dropna()
    
    return SectionData(rebar_data, section_data)


# Class for managing section data
class SectionData:
    """
    Class to manage reinforced concrete section data.
    """
    def __init__(self, rebar_df, section_df):
        """
        Initialize SectionData with rebar and section dataframes.
        
        Args:
            rebar_df: DataFrame with rebar coordinates (columns: RebarID, X, Y, Diameter, Grade)
            section_df: DataFrame with section coordinates (columns: point, x, y)
        """
        self.rebar_df = rebar_df
        self.section_df = section_df
        self.rebar_coor_data = self.get_rebar_coordinates()
        self.section_coor_data = self.get_section_coordinates()
        self.length_unit = None  # Default length unit
        self.force_unit = None  # Default force unit

    def set_units(self, length_unit, force_unit):
        """
        Set the units for length and force.
        
        Args:
            length_unit: Length unit (default: "None")
            force_unit: Force unit (default: "None")
        """
        self.length_unit = length_unit
        self.force_unit = force_unit
        
        # Create arrays with units (as Quantity objects for display)
        self.rebar_with_units = []
        for i in range(len(self.rebar_coor_data)):
            x_with_unit = Q_(self.rebar_coor_data[i, 0], self.length_unit)
            y_with_unit = Q_(self.rebar_coor_data[i, 1], self.length_unit)
            self.rebar_with_units.append([x_with_unit, y_with_unit])

        self.section_with_units = []
        for i in range(len(self.section_coor_data)):
            x_with_unit = Q_(self.section_coor_data[i, 0], self.length_unit)
            y_with_unit = Q_(self.section_coor_data[i, 1], self.length_unit)
            self.section_with_units.append([x_with_unit, y_with_unit])
        
        # Create arrays in SI base units (for calculations) - use np.array to create new array
        self.rebar = np.zeros_like(self.rebar_coor_data, dtype=float)
        self.section_polygon = np.zeros_like(self.section_coor_data, dtype=float)
        
        for i in range(len(self.rebar_coor_data)):
            self.rebar[i, 0] = Q_(self.rebar_coor_data[i, 0], self.length_unit).to_base_units().magnitude
            self.rebar[i, 1] = Q_(self.rebar_coor_data[i, 1], self.length_unit).to_base_units().magnitude

        for i in range(len(self.section_coor_data)):
            self.section_polygon[i, 0] = Q_(self.section_coor_data[i, 0], self.length_unit).to_base_units().magnitude
            self.section_polygon[i, 1] = Q_(self.section_coor_data[i, 1], self.length_unit).to_base_units().magnitude


    def display_info(self):
        """
        Display basic information about the section data.
        """
        if self.rebar_df.empty or self.section_df.empty:
            print("No data rebar coordinate or section coordinate available.")
            return
        elif self.length_unit is None or self.force_unit is None:
            print("Please set units using set_units() method before displaying info.")
            return

        print("length unit:", self.length_unit)
        print("force unit:", self.force_unit)
        print("\nRebar Data:")
        print(self.rebar_df.head())
        print("\nSection Data:")
        print(self.section_df.head())
        print("\nRebar Coordinates (original):")
        print(self.rebar_coor_data)
        print("\nSection Coordinates (original):")
        print(self.section_coor_data)
        print("\nRebar Coordinates with units:")
        for i, rebar in enumerate(self.rebar_with_units):
            print(f"  Rebar {i+1}: X = {rebar[0]:2f~P}, Y = {rebar[1]:2f~P}")
        print("\nSection Coordinates with units:")
        for i, point in enumerate(self.section_with_units):
            print(f"  Point {i+1}: x = {point[0]:2f~P}, y = {point[1]:2f~P}")
        print("\nRebar Coordinates (SI base units - meters):")
        print(self.rebar)
        print("\nSection Coordinates (SI base units - meters):")
        print(self.section_polygon)
        
    def get_rebar_coordinates(self):
        """
        Get rebar coordinates as numpy array.
        
        Returns:
            Numpy array of shape (n_rebars, 2) with X, Y coordinates
        """
        return self.rebar_df[['X', 'Y']].to_numpy()
    
    def get_section_coordinates(self):
        """
        Get section coordinates as numpy array.
        
        Returns:
            Numpy array of shape (n_points, 2) with x, y coordinates
        """
        return self.section_df[['x', 'y']].to_numpy()
    
    def get_rebar_details(self):
        """
        Get full rebar details including diameter and grade.
        
        Returns:
            DataFrame with all rebar information
        """
        return self.rebar_df
    
    def get_section_details(self):
        """
        Get full section details.
        
        Returns:
            DataFrame with all section information
        """
        return self.section_df