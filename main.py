import RCSectionDesigner as RCSD

def main():
    sectionData = RCSD.SectionData(con_matprop = 30) # concrete strength in MPa 
    sectionData.rotate_section(angle_degrees = 20)
    # sectionData.plot(is_rotated=False)
    # strainCompatibility_1 = RCSD.StrainCompatibility(sectionData, neutral_axis_y=0)  # neutral_axis_y
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
# เดี๋ยวต้องใช้ ทำ rebar cross section property และไป edit sectiondata.py ด้วย เพื่อให้ดึงขนาดเหล็กได้
# แล้วก็ต้องไป edit straincompatibility.py เพื่อคำนวณแรง rebar ให้ถูกต้อง