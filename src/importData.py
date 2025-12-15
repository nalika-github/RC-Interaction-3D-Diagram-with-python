import pandas as pd
import numpy as np
from . import config

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

def prepare_data(rebar_filepath=None, 
                 section_filepath=None):
    """
    Import and prepare both rebar and section coordinate data.
    
    Args:
        rebar_filepath: Path to the rebar coordinate CSV file (default: from config)
        section_filepath: Path to the section coordinate CSV file (default: from config)
        
    Returns:
        Tuple of (rebar_df, section_df) ready for use
    """
    rebar_data = import_rebar_coordinates(rebar_filepath)
    section_data = import_section_coordinates(section_filepath)
    
    # Clean data: remove NaN values
    rebar_data = rebar_data.dropna()
    section_data = section_data.dropna()
    
    return rebar_data, section_data