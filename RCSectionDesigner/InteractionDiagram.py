from . import StrainCompatibility
import matplotlib.pyplot as plt
import numpy as np

class InteractionDiagram:
    def __init__(self, section_data):
        self.section_data = section_data
        self.results = []

    def cal_2d_interaction_diagram(self, angle, n_points=100000):
        section = self.section_data

        # ใช้จุดหมุนเดียวกันสำหรับคอนกรีตและเหล็ก
        centroid = section.polygon.centroid
        origin = (centroid.x, centroid.y)

        section.rotate_section(
            angle_degrees=angle,
            origin=origin,
        )

        # ชื่อ _ แทน เป็นธรรมเนียมที่สื่อว่า “ค่านี้ไม่ต้องใช้” (min_x, min_y, max_x, max_y)
        _, bottom_y, _, top_y = section.ro_polygon.bounds
        height = top_y - bottom_y
        if height <= 0:
            raise ValueError("Section height must be positive.")

        # ช่วงเริ่มต้นสำหรับทดลอง ยังไม่ใช่จุดปลายแบบ exact
        c_values = height * np.geomspace(1e-4, 100, n_points) # สร้างตัวเลขตั้งแต่ 0.0001 ถึง 100 จำนวน n_points ค่า โดยแต่ละค่ามี อัตราส่วนต่อกันเท่ากัน
        points = []
        for point_id, c in enumerate(c_values):
            neutral_axis_y = top_y - c
            analysis = StrainCompatibility(
                section,
                neutral_axis_y=neutral_axis_y,
            )
            result = analysis.PM_Point()
            points.append({
                "angle": float(angle),
                "point_id": point_id,
                "c": float(c),  # หน่วยเดียวกับพิกัดหน้าตัด
                "P_n": result["P_n"].to("kN"),
                "M_n": result["M_n"].to("kN*m"),
            })

        self.results = points
        return points

    def plot_2d(self):
        if not self.results:
            raise ValueError(
                "Calculate the interaction diagram before plotting."
            )

        # ดึงผลแต่ละจุด และแปลงเป็นตัวเลขในหน่วยเดียวกัน
        moments = [
            point["M_n"].to("kN*m").magnitude
            for point in self.results
        ]

        axial_forces = [
            point["P_n"].to("kN").magnitude
            for point in self.results
        ]

        angle = self.results[0]["angle"]

        fig, ax = plt.subplots(figsize=(8, 6))

        # เชื่อมจุดตามลำดับ c ที่คำนวณไว้
        ax.plot(
            moments,
            axial_forces,
            color="blue",
            marker=".",
            markersize=3,
            linewidth=1.5,
            label=f"Rotation = {angle:g}°",
        )

        ax.axhline(0, color="gray", linewidth=0.8)
        ax.axvline(0, color="gray", linewidth=0.8)

        ax.set_xlabel("Moment about rotated x-axis (kN·m)")
        ax.set_ylabel("Axial force (kN), compression positive")
        ax.set_title("Nominal P–M Interaction Diagram")

        ax.grid(True, alpha=0.3)
        ax.legend()

        fig.tight_layout()
        plt.show()
        plt.close(fig)