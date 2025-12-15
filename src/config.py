"""
Configuration file for RC-InteractionD project.
Contains path configurations and constants.
"""

import os

# Base directory of the project (root directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directories
COORDINATE_DATA_DIR = os.path.join(BASE_DIR, 'coordinateData')
MATERIAL_DATA_DIR = os.path.join(BASE_DIR, 'materialData')

# Coordinate data files
REBAR_COORDINATE_FILE = os.path.join(COORDINATE_DATA_DIR, 'rebarCoordinate.csv')
SECTION_COORDINATE_FILE = os.path.join(COORDINATE_DATA_DIR, 'sectionCoordinate.csv')

# Material data files
REBAR_GRADE_FILE = os.path.join(MATERIAL_DATA_DIR, 'rebarGrade.csv')

# Constants (can be adjusted as needed)
DEFAULT_CONCRETE_STRENGTH = 28  # MPa (f'c)
DEFAULT_STEEL_YIELD_STRENGTH = 400  # MPa (fy for SD400)

# Analysis settings
ANALYSIS_POINTS = 50  # Number of points in interaction diagram
STRAIN_COMPRESSION_MAX = 0.003  # Maximum concrete strain
STRAIN_TENSION_YIELD = 0.002  # Steel yield strain for SD400

# Output settings
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

# Create output directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Debug mode
DEBUG = False

if __name__ == "__main__":
    # Print all paths for verification
    print("RC-InteractionD Configuration")
    print("=" * 50)
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"\nData Directories:")
    print(f"  COORDINATE_DATA_DIR: {COORDINATE_DATA_DIR}")
    print(f"  MATERIAL_DATA_DIR: {MATERIAL_DATA_DIR}")
    print(f"\nData Files:")
    print(f"  REBAR_COORDINATE_FILE: {REBAR_COORDINATE_FILE}")
    print(f"  SECTION_COORDINATE_FILE: {SECTION_COORDINATE_FILE}")
    print(f"  REBAR_GRADE_FILE: {REBAR_GRADE_FILE}")
    print(f"\nOutput Directories:")
    print(f"  OUTPUT_DIR: {OUTPUT_DIR}")
    print(f"  RESULTS_DIR: {RESULTS_DIR}")
    print("=" * 50)
    
    # Check if files exist
    print("\nFile Existence Check:")
    print(f"  Rebar coordinates: {os.path.exists(REBAR_COORDINATE_FILE)}")
    print(f"  Section coordinates: {os.path.exists(SECTION_COORDINATE_FILE)}")
    print(f"  Rebar grade: {os.path.exists(REBAR_GRADE_FILE)}")
