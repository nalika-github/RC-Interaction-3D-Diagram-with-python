# RC-InteractionD

โปรแกรมสำหรับวิเคราะห์ปฏิสัมพันธ์ของคอนกรีตเสริมเหล็ก (Reinforced Concrete Interaction Diagram)

## โครงสร้างโปรเจค

```
RC-InteractionD/
├── coordinateData/           # ข้อมูลพิกัดต่างๆ
│   ├── rebarCoordinate.csv   # พิกัดเหล็กเสริม (X, Y, เส้นผ่านศูนย์กลาง, เกรด)
│   └── sectionCoordinate.csv # พิกัดหน้าตัดคอนกรีต
├── materialData/             # ข้อมูลคุณสมบัติวัสดุ
│   └── rebarGrade.csv        # คุณสมบัติเกรดเหล็กเสริม
├── src/                      # Source code หลัก
│   ├── __init__.py           # Package initialization
│   ├── importData.py         # โมดูลสำหรับอ่านข้อมูล CSV
│   ├── material.py           # โมดูลคำนวณคุณสมบัติวัสดุ
│   ├── sectionCut.py         # โมดูลคำนวณหน้าตัด
│   └── config.py             # การตั้งค่า path และค่าคงที่
├── main.py                   # ไฟล์หลักสำหรับรันโปรแกรม
├── requirements.txt          # Python dependencies
├── .gitignore               # ไฟล์ที่ไม่ต้อง commit
└── README.md                # เอกสารนี้
```

## การติดตั้ง

### 1. Clone โปรเจค
```bash
git clone <repository-url>
cd RC-InteractionD
```

### 2. สร้าง Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # สำหรับ Linux/Mac
# หรือ venv\Scripts\activate  # สำหรับ Windows
```

### 3. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

## วิธีใช้งาน

### รันโปรแกรมหลัก
```bash
python3 main.py
```

### Import โมดูลในโค้ด
```python
from src import importData

# อ่านข้อมูลพิกัดเหล็กเสริมและหน้าตัด
rebar_data, section_data = importData.prepare_data()
print(rebar_data)
print(section_data)
```

## โมดูลหลัก

### importData.py
- `import_rebar_coordinates()`: อ่านข้อมูลพิกัดเหล็กเสริม
- `import_section_coordinates()`: อ่านข้อมูลพิกัดหน้าตัด
- `prepare_data()`: อ่านและเตรียมข้อมูลทั้งหมด

### material.py
- คำนวณคุณสมบัติวัสดุคอนกรีตและเหล็กเสริม

### sectionCut.py
- วิเคราะห์และคำนวณหน้าตัดคอนกรีตเสริมเหล็ก

## ข้อมูล CSV

### rebarCoordinate.csv
| Column | Description |
|--------|-------------|
| RebarID | รหัสเหล็กเสริม |
| X | พิกัด X (mm) |
| Y | พิกัด Y (mm) |
| Diameter | เส้นผ่านศูนย์กลาง (mm) |
| Grade | เกรดเหล็ก (เช่น SD400) |

### sectionCoordinate.csv
| Column | Description |
|--------|-------------|
| point | จุดที่ของหน้าตัด |
| x | พิกัด x (mm) |
| y | พิกัด y (mm) |

## เวอร์ชัน

- **v0.1.0** - เวอร์ชันเริ่มต้น

## ผู้พัฒนา

Project developed for RC interaction diagram analysis.

## License

-
