import math

# ==============================================================================
# 1. 用户配置区域 - 请在此处修改参数
# ==============================================================================

# --- 设置圆心坐标 (纬度, 经度) ---
# 您可以设为任何地点。这里提供几个示例：
# 北京故宫: 39.9163, 116.3972
# 西安钟楼: 34.2612, 108.9782
# 洛阳:     34.6254, 112.4536
CENTER_LATITUDE =  37.230048
CENTER_LONGITUDE = 115.017837

# --- 设置圆环半径 (单位：米) ---
# 可以根据需要调整大小，例如设为 10000 (10公里) 或 500000 (500公里)
RADIUS_METERS = 10  # 当前设置为100公里

# --- 设置输出文件名 ---
OUTPUT_KML_FILE = "celestial_stable_map.kml"


# ==============================================================================
# 2. KML生成逻辑 - 一般无需修改以下内容
# ==============================================================================

def create_kml_celestial_map(center_lat, center_lon, radius_m, file_name):
    """
    生成一个具有五行配色、北对齐、内外标注的二十八星宿KML文件。
    （基于稳定版设计进行功能升级）
    """
    
    # --- 数据定义 ---
    mansions_data = [
        ("虚", 0, 7.5), ("女", 7.5, 22.5), ("牛", 22.5, 37.5), ("斗", 37.5, 52.5),
        ("箕", 52.5, 67.5), ("尾", 67.5, 82.5), ("心", 82.5, 90), ("房", 90, 97.5),
        ("氐", 97.5, 112.5), ("亢", 112.5, 127.5), ("角", 127.5, 142.5), ("轸", 142.5, 157.5),
        ("翼", 157.5, 172.5), ("张", 172.5, 180), ("星", 180, 187.5), ("柳", 187.5, 202.5),
        ("鬼", 202.5, 217.5), ("井", 217.5, 232.5), ("参", 232.5, 247.5), ("觜", 247.5, 262.5),
        ("毕", 262.5, 270), ("昴", 270, 277.5), ("胃", 277.5, 292.5), ("娄", 292.5, 307.5),
        ("奎", 307.5, 322.5), ("壁", 322.5, 337.5), ("室", 337.5, 352.5), ("危", 352.5, 360)
    ]
    
    elements_map = {
        "虚": "日", "女": "土", "牛": "金", "斗": "木", "箕": "水", "尾": "火", "心": "月",
        "房": "日", "氐": "土", "亢": "金", "角": "木", "轸": "水", "翼": "火", "张": "月",
        "星": "日", "柳": "土", "鬼": "金", "井": "木", "参": "水", "觜": "火", "毕": "月",
        "昴": "日", "胃": "土", "娄": "金", "奎": "木", "壁": "水", "室": "火", "危": "月"
    }
    
    element_colors = {
        "木": "8078AB00", "火": "801F25D9", "土": "8000A5FF", "金": "80E0E0E0", "水": "80D07000"
    }

    # --- 辅助函数 (已修正和优化) ---
    EARTH_RADIUS = 6378137.0
    def get_destination_point(start_lat, start_lon, bearing, distance):
        brng = math.radians(bearing)
        d = distance / EARTH_RADIUS
        lat1 = math.radians(start_lat)
        lon1 = math.radians(start_lon)
        lat2 = math.asin(math.sin(lat1) * math.cos(d) + math.cos(lat1) * math.sin(d) * math.cos(brng))
        lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d) * math.cos(lat1), math.cos(d) - math.sin(lat1) * math.sin(lat2))
        return (math.degrees(lat2), math.degrees(lon2))

    # --- KML文件内容生成 ---
    kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>二十八星宿五行图 (稳定修复版)</name>
    <description>采用五行配色，0度对齐正北，并标注星宿的五行/七曜属性。</description>
"""
    # --- 定义样式 ---
    for element, color in element_colors.items():
        kml_content += f"""
    <Style id="style{element}">
      <LineStyle><width>1.5</width><color>c0ffffff</color></LineStyle>
      <PolyStyle><color>{color}</color></PolyStyle>
    </Style>"""
    kml_content += """
    <Style id="styleMansionLabel"><IconStyle><scale>0</scale></IconStyle><LabelStyle><color>ffffffff</color><scale>0.9</scale></LabelStyle></Style>
    <Style id="styleAngleLabel"><IconStyle><scale>0</scale></IconStyle><LabelStyle><color>ff00ffff</color><scale>1.0</scale></LabelStyle></Style>"""

    # --- 创建KML文件夹和Placemarks ---
    center_point_str = f"{center_lon},{center_lat},0"
    
    # 1. 扇区文件夹
    kml_content += "\n    <Folder><name>星宿扇区 (五行)</name>"
    for (name, start_deg, end_deg) in mansions_data:
        element = elements_map.get(name, "")
        color_element = "火" if element in ["日", "月"] else element
        style_url = f"#style{color_element}"
        placemark_name = f"{name} ({element})" if element else name
        
        coords = [center_point_str]
        deg_step = max((end_deg - start_deg) / 10, 0.5)
        current_deg = start_deg
        while current_deg < end_deg:
            dest_lat, dest_lon = get_destination_point(center_lat, center_lon, current_deg, radius_m)
            coords.append(f"{dest_lon},{dest_lat},0")
            current_deg += deg_step
        dest_lat, dest_lon = get_destination_point(center_lat, center_lon, end_deg, radius_m)
        coords.append(f"{dest_lon},{dest_lat},0")
        coords.append(center_point_str)
        coords_str = " ".join(coords)
        
        kml_content += f"""
      <Placemark>
        <name>{placemark_name}</name>
        <styleUrl>{style_url}</styleUrl>
        <Polygon><altitudeMode>clampToGround</altitudeMode><outerBoundaryIs><LinearRing><coordinates>{coords_str}</coordinates></LinearRing></outerBoundaryIs></Polygon>
      </Placemark>"""
    kml_content += "\n    </Folder>"

    # 2. 星宿名称标签文件夹
    kml_content += "\n    <Folder><name>星宿名称</name>"
    label_radius = radius_m * 0.7
    for name, start_deg, end_deg in mansions_data:
        element = elements_map.get(name, "")
        label_text = f"{name}\n({element})" if element else name
        mid_deg = (start_deg + end_deg) / 2.0
        dest_lat, dest_lon = get_destination_point(center_lat, center_lon, mid_deg, label_radius)
        coords_str = f"{dest_lon},{dest_lat},0"
        kml_content += f"""
      <Placemark><name>{label_text}</name><styleUrl>#styleMansionLabel</styleUrl><Point><altitudeMode>clampToGround</altitudeMode><coordinates>{coords_str}</coordinates></Point></Placemark>"""
    kml_content += "\n    </Folder>"
    
    # 3. 外部角度环文件夹
    kml_content += "\n    <Folder><name>外部角度环</name>"
    angle_label_radius = radius_m * 1.15
    for angle in range(0, 360, 15):
        dest_lat, dest_lon = get_destination_point(center_lat, center_lon, angle, angle_label_radius)
        coords_str = f"{dest_lon},{dest_lat},0"
        kml_content += f"""
      <Placemark><name>{angle}°</name><styleUrl>#styleAngleLabel</styleUrl><Point><altitudeMode>clampToGround</altitudeMode><coordinates>{coords_str}</coordinates></Point></Placemark>"""
    kml_content += "\n    </Folder>"
    
    kml_content += """
  </Document>
</kml>
"""
    # 写入文件
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(kml_content)
        print(f"成功！文件 '{file_name}' 已在当前目录生成。")
        print(f"配置: 中心=({center_lat}, {center_lon}), 半径={radius_m}米")
    except Exception as e:
        print(f"错误：无法写入文件。{e}")


# ==============================================================================
# 3. 运行主程序
# ==============================================================================
if __name__ == "__main__":
    create_kml_celestial_map(
        center_lat=CENTER_LATITUDE,
        center_lon=CENTER_LONGITUDE,
        radius_m=RADIUS_METERS,
        file_name=OUTPUT_KML_FILE
    )