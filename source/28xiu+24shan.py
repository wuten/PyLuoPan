import math

# ==============================================================================
# 1. 用户配置区域 - 请在此处修改参数
# ==============================================================================

# --- 设置圆心坐标 (纬度, 经度) ---
CENTER_LATITUDE = 39.9163  # 北京故宫
CENTER_LONGITUDE = 116.3972

# --- 设置双环参数 (单位：米 或 百分比) ---
RING_1_OUTER_RADIUS_METERS = 100000  # 外环(二十八宿)的外部半径
RING_1_THICKNESS_PERCENT = 25       # 外环的厚度百分比
GAP_BETWEEN_RINGS_PERCENT = 5       # 内外环之间的间距百分比
RING_2_THICKNESS_PERCENT = 25       # 内环(二十四山)的厚度百分比

# --- 设置输出文件名 ---
OUTPUT_KML_FILE = "celestial_final_map.kml"


# ==============================================================================
# 2. KML生成逻辑 - 一般无需修改以下内容
# ==============================================================================

def create_kml_dual_ring(center_lat, center_lon, r1_outer_m, r1_thick_pct, gap_pct, r2_thick_pct, file_name):
    """
    生成一个包含二十八宿环和二十四山内环，并带有中心十字的双环KML图谱。
    """
    
    # --- 数据定义 ---
    # 环1: 二十八宿 (数据不变)
    mansions_data = [
        ("虚", 0, 7.5), ("女", 7.5, 22.5), ("牛", 22.5, 37.5), ("斗", 37.5, 52.5), ("箕", 52.5, 67.5), 
        ("尾", 67.5, 82.5), ("心", 82.5, 90), ("房", 90, 97.5), ("氐", 97.5, 112.5), ("亢", 112.5, 127.5),
        ("角", 127.5, 142.5), ("轸", 142.5, 157.5), ("翼", 157.5, 172.5), ("张", 172.5, 180), ("星", 180, 187.5),
        ("柳", 187.5, 202.5), ("鬼", 202.5, 217.5), ("井", 217.5, 232.5), ("参", 232.5, 247.5), ("觜", 247.5, 262.5),
        ("毕", 262.5, 270), ("昴", 270, 277.5), ("胃", 277.5, 292.5), ("娄", 292.5, 307.5), ("奎", 307.5, 322.5),
        ("壁", 322.5, 337.5), ("室", 337.5, 352.5), ("危", 352.5, 360)
    ]
    elements_map = {
        "虚": "日", "女": "土", "牛": "金", "斗": "木", "箕": "水", "尾": "火", "心": "月", "房": "日", "氐": "土", "亢": "金",
        "角": "木", "轸": "水", "翼": "火", "张": "月", "星": "日", "柳": "土", "鬼": "金", "井": "木", "参": "水", "觜": "火",
        "毕": "月", "昴": "日", "胃": "土", "娄": "金", "奎": "木", "壁": "水", "室": "火", "危": "月"
    }
    element_colors = {"木": "6078AB00", "火": "601F25D9", "土": "6000A5FF", "金": "60E0E0E0", "水": "60D07000"}

    # 环2: 二十四山 (MODIFIED: 更新"子"的数据)
    mountains_data = [
        ("癸", 7.5, 22.5), ("丑", 22.5, 37.5), ("艮", 37.5, 52.5), ("寅", 52.5, 67.5), ("甲", 67.5, 82.5),
        ("卯", 82.5, 97.5), ("乙", 97.5, 112.5), ("辰", 112.5, 127.5), ("巽", 127.5, 142.5), ("巳", 142.5, 157.5),
        ("丙", 157.5, 172.5), ("午", 172.5, 187.5), ("丁", 187.5, 202.5), ("未", 202.5, 217.5), ("坤", 217.5, 232.5),
        ("申", 232.5, 247.5), ("庚", 247.5, 262.5), ("酉", 262.5, 277.5), ("辛", 277.5, 292.5), ("戌", 292.5, 307.5),
        ("乾", 307.5, 322.5), ("亥", 322.5, 337.5), ("壬", 337.5, 352.5),
        ("子", 352.5, 7.5) # 更新了此条数据以跨越0度
    ]
    mountain_colors = ["60808080", "60A0A0A0"]

    # --- 动态计算所有半径 ---
    r1_inner_m = r1_outer_m * (1 - r1_thick_pct / 100.0); gap_m = r1_outer_m * (gap_pct / 100.0)
    r2_outer_m = r1_inner_m - gap_m; r2_inner_m = r2_outer_m * (1 - r2_thick_pct / 100.0)

    # --- 辅助函数 ---
    EARTH_RADIUS = 6378137.0
    def get_destination_point(start_lat, start_lon, bearing, distance):
        brng = math.radians(bearing); d = distance / EARTH_RADIUS; lat1 = math.radians(start_lat); lon1 = math.radians(start_lon)
        lat2 = math.asin(math.sin(lat1) * math.cos(d) + math.cos(lat1) * math.sin(d) * math.cos(brng))
        lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d) * math.cos(lat1), math.cos(d) - math.sin(lat1) * math.sin(lat2))
        return (math.degrees(lat2), math.degrees(lon2))

    def create_ring_segment_coords(center_lat, center_lon, outer_r, inner_r, start_deg, end_deg):
        coords = []; deg_step = 0.5
        
        # 外环弧线
        current_deg = start_deg
        # MODIFIED: 处理跨0度的情况
        end_loop_deg = end_deg if start_deg < end_deg else 360.0
        while current_deg < end_loop_deg:
            lat, lon = get_destination_point(center_lat, center_lon, current_deg, outer_r); coords.append(f"{lon},{lat},0")
            current_deg += deg_step
        if start_deg > end_deg: # 如果是跨0度，继续画0到终点的部分
            current_deg = 0.0
            while current_deg < end_deg:
                lat, lon = get_destination_point(center_lat, center_lon, current_deg, outer_r); coords.append(f"{lon},{lat},0")
                current_deg += deg_step
        lat, lon = get_destination_point(center_lat, center_lon, end_deg, outer_r); coords.append(f"{lon},{lat},0")
        
        # 内环弧线 (逻辑类似，但方向相反)
        current_deg = end_deg
        start_loop_deg = start_deg if start_deg < end_deg else 0.0
        while current_deg > start_loop_deg:
            lat, lon = get_destination_point(center_lat, center_lon, current_deg, inner_r); coords.append(f"{lon},{lat},0")
            current_deg -= deg_step
        if start_deg > end_deg: # 如果是跨0度，继续画360到起点的部分
            current_deg = 360.0
            while current_deg > start_deg:
                lat, lon = get_destination_point(center_lat, center_lon, current_deg, inner_r); coords.append(f"{lon},{lat},0")
                current_deg -= deg_step
        lat, lon = get_destination_point(center_lat, center_lon, start_deg, inner_r); coords.append(f"{lon},{lat},0")
        
        coords.append(coords[0]) # 闭合
        return " ".join(coords)

    # --- KML文件内容生成 ---
    kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>二十八宿与二十四山双环图 (最终版)</name>
    <description>外环为二十八宿，内环为二十四山，带中心十字。</description>"""
    
    # --- 定义样式 ---
    for e, c in element_colors.items(): kml_content += f'\n<Style id="style{e}"><LineStyle><width>1.2</width><color>c0ffffff</color></LineStyle><PolyStyle><color>{c}</color></PolyStyle></Style>'
    for i, c in enumerate(mountain_colors): kml_content += f'\n<Style id="styleMountain{i}"><LineStyle><width>1</width><color>a0ffffff</color></LineStyle><PolyStyle><color>{c}</color></PolyStyle></Style>'
    kml_content += """
    <Style id="styleMansionLabel"><IconStyle><scale>0</scale></IconStyle><LabelStyle><color>ffffffff</color><scale>0.9</scale></LabelStyle></Style>
    <Style id="styleMountainLabel"><IconStyle><scale>0</scale></IconStyle><LabelStyle><color>ffeeeeee</color><scale>0.75</scale></LabelStyle></Style>
    <Style id="styleAngleLabel"><IconStyle><scale>0</scale></IconStyle><LabelStyle><color>ff00ffff</color><scale>1.0</scale></LabelStyle></Style>
    <Style id="styleCrosshair"><LineStyle><color>ffffffff</color><width>1.5</width></LineStyle></Style>"""

    # --- 创建KML文件夹和Placemarks ---
    # NEW: 中心十字文件夹
    kml_content += "\n<Folder><name>中心十字</name>"
    cross_r = r2_inner_m * 0.9 # 十字线半径
    lat_n, lon_n = get_destination_point(center_lat, center_lon, 0, cross_r)
    lat_s, lon_s = get_destination_point(center_lat, center_lon, 180, cross_r)
    lat_e, lon_e = get_destination_point(center_lat, center_lon, 90, cross_r)
    lat_w, lon_w = get_destination_point(center_lat, center_lon, 270, cross_r)
    kml_content += f"""
      <Placemark><name>南北线</name><styleUrl>#styleCrosshair</styleUrl><LineString><altitudeMode>clampToGround</altitudeMode><coordinates>{lon_n},{lat_n},0 {lon_s},{lat_s},0</coordinates></LineString></Placemark>
      <Placemark><name>东西线</name><styleUrl>#styleCrosshair</styleUrl><LineString><altitudeMode>clampToGround</altitudeMode><coordinates>{lon_e},{lat_e},0 {lon_w},{lat_w},0</coordinates></LineString></Placemark>"""
    kml_content += "\n</Folder>"

    # 外环: 二十八宿
    kml_content += "\n<Folder><name>外环：二十八宿</name>"
    for name, start_deg, end_deg in mansions_data:
        element = elements_map.get(name, ""); color_element = "火" if element in ["日", "月"] else element
        coords_str = create_ring_segment_coords(center_lat, center_lon, r1_outer_m, r1_inner_m, start_deg, end_deg)
        kml_content += f'\n<Placemark><name>{name} ({element})</name><styleUrl>#style{color_element}</styleUrl><Polygon><altitudeMode>clampToGround</altitudeMode><outerBoundaryIs><LinearRing><coordinates>{coords_str}</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'
        mid_deg = ((start_deg + end_deg) / 2) if start_deg < end_deg else (((start_deg + end_deg + 360) / 2) % 360)
        lat, lon = get_destination_point(center_lat, center_lon, mid_deg, (r1_outer_m + r1_inner_m) / 2)
        kml_content += f'\n<Placemark><name>{name}\n({element})</name><styleUrl>#styleMansionLabel</styleUrl><Point><altitudeMode>clampToGround</altitudeMode><coordinates>{lon},{lat},0</coordinates></Point></Placemark>'
    kml_content += "\n</Folder>"

    # 内环: 二十四山
    kml_content += "\n<Folder><name>内环：二十四山</name>"
    for i, (name, start_deg, end_deg) in enumerate(mountains_data):
        style_url = f"#styleMountain{i % len(mountain_colors)}"
        coords_str = create_ring_segment_coords(center_lat, center_lon, r2_outer_m, r2_inner_m, start_deg, end_deg)
        kml_content += f'\n<Placemark><name>{name}</name><styleUrl>{style_url}</styleUrl><Polygon><altitudeMode>clampToGround</altitudeMode><outerBoundaryIs><LinearRing><coordinates>{coords_str}</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'
        mid_deg = ((start_deg + end_deg) / 2) if start_deg < end_deg else (((start_deg + end_deg + 360) / 2) % 360)
        lat, lon = get_destination_point(center_lat, center_lon, mid_deg, (r2_outer_m + r2_inner_m) / 2)
        kml_content += f'\n<Placemark><name>{name}</name><styleUrl>#styleMountainLabel</styleUrl><Point><altitudeMode>clampToGround</altitudeMode><coordinates>{lon},{lat},0</coordinates></Point></Placemark>'
    kml_content += "\n</Folder>"
    
    # 外部角度环
    kml_content += "\n<Folder><name>最外层角度环</name>"
    for angle in range(0, 360, 15):
        lat, lon = get_destination_point(center_lat, center_lon, angle, r1_outer_m * 1.15)
        kml_content += f'\n<Placemark><name>{angle}°</name><styleUrl>#styleAngleLabel</styleUrl><Point><altitudeMode>clampToGround</altitudeMode><coordinates>{lon},{lat},0</coordinates></Point></Placemark>'
    kml_content += "\n</Folder>"
    
    kml_content += """\n</Document>\n</kml>"""
    # 写入文件
    try:
        with open(file_name, 'w', encoding='utf-8') as f: f.write(kml_content)
        print(f"成功！文件 '{file_name}' 已在当前目录生成。"); print(f"配置: 中心=({center_lat}, {center_lon}), 外环半径={r1_outer_m}米")
    except Exception as e: print(f"错误：无法写入文件。{e}")

# ==============================================================================
# 3. 运行主程序
# ==============================================================================
if __name__ == "__main__":
    create_kml_dual_ring(
        center_lat=CENTER_LATITUDE,
        center_lon=CENTER_LONGITUDE,
        r1_outer_m=RING_1_OUTER_RADIUS_METERS,
        r1_thick_pct=RING_1_THICKNESS_PERCENT,
        gap_pct=GAP_BETWEEN_RINGS_PERCENT,
        r2_thick_pct=RING_2_THICKNESS_PERCENT,
        file_name=OUTPUT_KML_FILE
    )