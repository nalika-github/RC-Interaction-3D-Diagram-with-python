import RCSectionDesigner as RCSD

def main():
    sectionData = RCSD.SectionData(con_matprop = 30) # concrete strength in MPa 
    strainCompatibility_1 = RCSD.StrainCompatibility(sectionData, cut_y=100)  # cut_y in SI units (meters)
    strainCompatibility_1.plot()
    # interactionDiagram = RCSD.interactionDiagram(sectionData)
    # interactionDiagram.plot()
    # build_rotated_section(polyline, angle_degrees, section_name=None, origin='center')
    # print("Original section:")
    # sectionData.display_info()
    # print("Rotating section by 30 degrees...")
    # sectionData.rotate_section(angle_degrees=30)
    # print("Rotated section:")
    # print(sectionData.ro_polygon)
    # sectionData.plot(is_rotated=False)
    # sectionData.plot(is_rotated=True)
    # strainCompatibility_2 = RCSD.StrainCompatibility(sectionData, cut_y=100)
    # strainCompatibility_2.plot()

if __name__ == "__main__":
    main()

# เดี๋ยวต้องใช้ Plotly ทำ 3D Visualization ต่อ