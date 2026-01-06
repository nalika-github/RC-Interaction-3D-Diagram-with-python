from matplotlib.patches import Circle, Polygon
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plot_rc_section(sectionData):
    """
    Plot the reinforced concrete section with concrete and rebar coordinates.
    
    Args:
        sectionData: SectionData object containing section_polygon and rebar_coor_data
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Extract coordinates from sectionData
    concreteCoordinateArray = np.array(sectionData.section_polygon.exterior.coords)
    rebarCoordinateArray = sectionData.rebar_coor_data
    
    # Plot concrete section as polygon from coordinates
    concrete_polygon = Polygon(concreteCoordinateArray, 
                               linewidth=2, 
                               edgecolor='black', 
                               facecolor='lightgray', 
                               alpha=0.5,
                               closed=True)
    ax.add_patch(concrete_polygon)

    # Get bounds from actual coordinates
    min_x, min_y = np.min(concreteCoordinateArray, axis=0)
    max_x, max_y = np.max(concreteCoordinateArray, axis=0)
    width = max_x - min_x
    height = max_y - min_y
    
    # Calculate appropriate rebar radius (based on section size)
    rebar_radius = min(width, height) * 0.02  # 2% of smaller dimension
    
    # Plot rebar positions
    for coord in rebarCoordinateArray:
        rebar_patch = Circle((coord[0], coord[1]), radius=rebar_radius, color='red', alpha=0.8)
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