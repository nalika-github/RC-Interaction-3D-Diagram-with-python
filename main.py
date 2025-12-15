from src import importData
from src import material
from src import sectionCut
from src import plotRCSection
from src import ureg, Q_


def main():
    section_data = importData.prepare_data()
    section_data.set_units(length_unit="mm", force_unit="kN")
    section_data.display_info()
    plotRCSection.plot_rc_section(section_data.section_polygon, section_data.rebar)

 
if __name__ == "__main__":
    main()