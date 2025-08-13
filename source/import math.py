import math

def create_kml_circle_with_ticks(center_lon, center_lat, radius_m, tick_length_m, num_ticks, file_name):
    """
    生成一个包含带刻度的圆的KML文件。

    参数:
    center_lon (float): 圆心经度
    center_lat (float): 圆心纬度
    radius_m (float): 圆的半径 (米)
    tick_length_m (float): 刻度线长度 (米)
    num_ticks (int): 刻度线总数 (例如 36，即每10度一个)
    file_name (str): 输出的KML文件名
    """
    
    # 地球半径 (米)
    EARTH_RADIUS = 6378137.0

    def get_destination_point(lon, lat, bearing, distance):
        """
        根据起点、方位角和距离计算目标点的经纬度。
        """
        brng = math.radians(bearing)
        d = distance / EARTH_RADIUS

        lat1 = math.radians(lat)
        lon1 = math.radians(lon)

        lat2 = math.asin(math.sin(lat1) * math.cos(d) +
                         math.cos(lat1) * math.sin(d) * math.cos(brng))
        lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d) * math.cos(lat1),
                                  math.cos(d) - math.sin(lat1) * math.sin(lat2))

        return (math.degrees(lon2), math.degrees(lat2))

    # --- KML 文件头部 ---
    kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>带刻度的圆</name>
    <description>中心: ({center_lon}, {center_lat}), 半径: {radius_m}米</description>

    <Style id="circleStyle">
      <PolyStyle>
        <color>7d00ff00</color>
        <outline>1</outline>
      </PolyStyle>
      <LineStyle>
        <color>ff00aa00</color>
        <width>2</width>
      </LineStyle>
    </Style>
    <Style id="majorTickStyle">
      <LineStyle>
        <color>ff0000ff</color>
        <width>4</width>
      </LineStyle>
    </Style>
    <Style id="minorTickStyle">
      <LineStyle>
        <color>ffffaa00</color>
        <width>2.5</width>
      </LineStyle>
    </Style>

    <Folder>
      <name>图形元素</name>
      
      <Placemark>
        <name>圆</name>
        <styleUrl>#circleStyle</styleUrl>
        <Polygon>
          <altitudeMode>clampToGround</altitudeMode>
          <outerBoundaryIs>
            <LinearRing>
              <coordinates>
"""
    # 计算圆的顶点坐标
    circle_coords = []
    for i in range(361): # 361个点以确保多边形闭合
        lon, lat = get_destination_point(center_lon, center_lat, i, radius_m)
        circle_coords.append(f"{lon},{lat},0")
    kml_content += " ".join(circle_coords)
    
    kml_content += """
              </coordinates>
            </LinearRing>
          </outerBoundaryIs>
        </Polygon>
      </Placemark>

      """
    # 计算并添加刻度线
    for i in range(num_ticks):
        angle = (360 / num_ticks) * i
        
        # 判断是主要刻度还是次要刻度
        is_major = (angle % 90 == 0)
        style_url = "#majorTickStyle" if is_major else "#minorTickStyle"
        label = f"{int(angle)}°" if is_major else ""

        # 计算刻度线的起点和终点
        start_lon, start_lat = get_destination_point(center_lon, center_lat, angle, radius_m)
        end_lon, end_lat = get_destination_point(center_lon, center_lat, angle, radius_m + tick_length_m)
        
        tick_coords = f"{start_lon},{start_lat},0 {end_lon},{end_lat},0"

        kml_content += f"""
      <Placemark>
        <name>{label}</name>
        <styleUrl>{style_url}</styleUrl>
        <LineString>
          <altitudeMode>clampToGround</altitudeMode>
          <coordinates>{tick_coords}</coordinates>
        </LineString>
      </Placemark>
"""

    # --- KML 文件尾部 ---
    kml_content += """
    </Folder>
  </Document>
</kml>
"""
    # 写入文件
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(kml_content)
    print(f"文件 '{file_name}' 已成功生成！")


# --- 参数设置 ---
# 中心点坐标 (北京天安门广场)
CENTER_LONGITUDE = 116.391275
CENTER_LATITUDE = 39.907335

# 圆的半径 (米)
RADIUS_METERS = 1000

# 刻度线长度 (米)
TICK_LENGTH_METERS = 200 # 主刻度会长一些，这里是基础长度

# 刻度线数量 (36 表示每 10 度一个)
NUMBER_OF_TICKS = 36

# 输出文件名
OUTPUT_KML_FILE = "circle_with_ticks.kml"

# --- 运行脚本 ---
create_kml_circle_with_ticks(
    CENTER_LONGITUDE,
    CENTER_LATITUDE,
    RADIUS_METERS,
    TICK_LENGTH_METERS,
    NUMBER_OF_TICKS,
    OUTPUT_KML_FILE
)