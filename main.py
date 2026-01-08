import RCSectionDesigner as RCSD

def main():
    sectionData = RCSD.SectionData(con_matprop = 30) # concrete strength in MPa 
    sectionData.rotate_section(angle_degrees = 20)
    # sectionData.plot(is_rotated=False)
    strainCompatibility_1 = RCSD.StrainCompatibility(sectionData, neutral_axis_y=0)  # neutral_axis_y
    print("Rebar Forces at Neutral Axis y=0:")
    print(strainCompatibility_1.rebar_force)
    print("Total Axial Force and Moment:")
    print(strainCompatibility_1.PM_Point())
    strainCompatibility_1.plot_PMM()
    # print("Compression Rebar Coordinates:", strainCompatibility_1.compression_rebar)
    # strainCompatibility_1.plot()
    # print(strainCompatibility_1.PM_Point())
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

# Self Note:
# แล้วก็ต้องไป edit straincompatibility.py เพื่อคำนวณแรง rebar ให้ถูกต้อง
# restructure section data ใน straincompatibility.py ให้เป็น self attributes ให้หมดเลย จะได้ไม่ต้องส่ง section data ไปมา