import math

# ==============================================================================
# 1. 用户配置区域 - 请在此处修改参数
# ==============================================================================

# --- 设置圆心坐标 (纬度, 经度) ---
CENTER_LATITUDE =  39.911198  # 北京故宫
CENTER_LONGITUDE = 116.380719

# --- 设置四环参数 (单位：米 或 百分比) ---
RING_1_OUTER_RADIUS_METERS = 1000 # 环1 (最外层: 二十八宿) 的外部半径
RING_1_THICKNESS_PERCENT = 20       # 环1 的厚度
GAP_1_2_PERCENT = 5                 # 环1和环2之间的间距
RING_2_THICKNESS_PERCENT = 20       # 环2 (中层: 二十四山) 的厚度
GAP_2_3_PERCENT = 5                 # 环2和环3之间的间距
RING_3_THICKNESS_PERCENT = 20       # 环3 (内层: 十二地支) 的厚度
GAP_3_4_PERCENT = 5                 # 环3和环4之间的间距
RING_4_THICKNESS_PERCENT = 15       # 环4 (最内层: 八卦) 的厚度

# --- 设置输出文件名 ---
OUTPUT_KML_FILE = "celestial_final_map_v11.kml"


# ==============================================================================
# 2. KML生成逻辑 - 一般无需修改以下内容
# ==============================================================================

def create_kml_ultimate_map(center_lat, center_lon, r1_outer_m, r1_thick_pct, gap12_pct, r2_thick_pct, gap23_pct, r3_thick_pct, gap34_pct, r4_thick_pct, file_name):
    """
    生成一个具有四层同心环并极度优化文字显示的KML图谱。
    """
    
    # --- 数据定义 ---
    # 环1: 二十八宿 (不变)
    mansions_data = [("虚",0,7.5),("女",7.5,22.5),("牛",22.5,37.5),("斗",37.5,52.5),("箕",52.5,67.5),("尾",67.5,82.5),("心",82.5,90),("房",90,97.5),("氐",97.5,112.5),("亢",112.5,127.5),("角",127.5,142.5),("轸",142.5,157.5),("翼",157.5,172.5),("张",172.5,180),("星",180,187.5),("柳",187.5,202.5),("鬼",202.5,217.5),("井",217.5,232.5),("参",232.5,247.5),("觜",247.5,262.5),("毕",262.5,270),("昴",270,277.5),("胃",277.5,292.5),("娄",292.5,307.5),("奎",307.5,322.5),("壁",322.5,337.5),("室",337.5,352.5),("危",352.5,360)]
    elements_map = {"虚":"日","女":"土","牛":"金","斗":"木","箕":"水","尾":"火","心":"月","房":"日","氐":"土","亢":"金","角":"木","轸":"水","翼":"火","张":"月","星":"日","柳":"土","鬼":"金","井":"木","参":"水","觜":"火","毕":"月","昴":"日","胃":"土","娄":"金","奎":"木","壁":"水","室":"火","危":"月"}
    element_colors = {"木":"6078AB00","火":"601F25D9","土":"6000A5FF","金":"60E0E0E0","水":"60D07000"}

    # 环2: 二十四山 (不变)
    mountains_data = [("癸",7.5,22.5),("丑",22.5,37.5),("艮",37.5,52.5),("寅",52.5,67.5),("甲",67.5,82.5),("卯",82.5,97.5),("乙",97.5,112.5),("辰",112.5,127.5),("巽",127.5,142.5),("巳",142.5,157.5),("丙",157.5,172.5),("午",172.5,187.5),("丁",187.5,202.5),("未",202.5,217.5),("坤",217.5,232.5),("申",232.5,247.5),("庚",247.5,262.5),("酉",262.5,277.5),("辛",277.5,292.5),("戌",292.5,307.5),("乾",307.5,322.5),("亥",322.5,337.5),("壬",337.5,352.5),("子",352.5,7.5)]
    mountain_colors = ["60808080","60A0A0A0"]

    # 环3: 十二地支 (不变)
    branches_data = [("丑",15,45),("寅",45,75),("卯",75,105),("辰",105,135),("巳",135,165),("午",165,195),("未",195,225),("申",225,255),("酉",255,285),("戌",285,315),("亥",315,345),("子",345,15)]
    branch_colors = ["606A4982", "608355A0"]

    # 环4: 八卦 (MODIFIED: 更新为最新的八卦数据)
    gua_data = [
        ("坎", 337.5, 22.5), ("艮", 22.5, 67.5), ("震", 67.5, 112.5),
        ("巽", 112.5, 157.5), ("离", 157.5, 202.5), ("坤", 202.5, 247.5),
        ("兑", 247.5, 292.5), ("乾", 292.5, 337.5)
    ]
    gua_colors = ["60334C66", "604A6680"]

    # --- 动态计算所有半径 ---
    r1_inner_m=r1_outer_m*(1-r1_thick_pct/100.0); gap12_m=r1_outer_m*(gap12_pct/100.0); r2_outer_m=r1_inner_m-gap12_m
    r2_inner_m=r2_outer_m*(1-r2_thick_pct/100.0); gap23_m=r1_outer_m*(gap23_pct/100.0); r3_outer_m=r2_inner_m-gap23_m
    r3_inner_m=r3_outer_m*(1-r3_thick_pct/100.0); gap34_m=r1_outer_m*(gap34_pct/100.0); r4_outer_m=r3_inner_m-gap34_m
    r4_inner_m=r4_outer_m*(1-r4_thick_pct/100.0)

    # --- 辅助函数 ---
    EARTH_RADIUS=6378137.0
    def get_destination_point(lat,lon,bearing,dist):
        brng=math.radians(bearing);d=dist/EARTH_RADIUS;lat1=math.radians(lat);lon1=math.radians(lon)
        lat2=math.asin(math.sin(lat1)*math.cos(d)+math.cos(lat1)*math.sin(d)*math.cos(brng));lon2=lon1+math.atan2(math.sin(brng)*math.sin(d)*math.cos(lat1),math.cos(d)-math.sin(lat1)*math.sin(lat2))
        return (math.degrees(lat2),math.degrees(lon2))

    def create_ring_segment_coords(lat,lon,r_outer,r_inner,start,end):
        coords=[];step=0.5;current=start;end_loop=end if start<end else 360.0
        while current<end_loop:lat_n,lon_n=get_destination_point(lat,lon,current,r_outer);coords.append(f"{lon_n},{lat_n},0");current+=step
        if start>end:
            current=0.0
            while current<end:lat_n,lon_n=get_destination_point(lat,lon,current,r_outer);coords.append(f"{lon_n},{lat_n},0");current+=step
        lat_n,lon_n=get_destination_point(lat,lon,end,r_outer);coords.append(f"{lon_n},{lat_n},0");current=end
        start_loop=start if start<end else 0.0
        while current>start_loop:lat_n,lon_n=get_destination_point(lat,lon,current,r_inner);coords.append(f"{lon_n},{lat_n},0");current-=step
        if start>end:
            current=360.0
            while current>start:lat_n,lon_n=get_destination_point(lat,lon,current,r_inner);coords.append(f"{lon_n},{lat_n},0");current-=step
        lat_n,lon_n=get_destination_point(lat,lon,start,r_inner);coords.append(f"{lon_n},{lat_n},0");coords.append(coords[0])
        return " ".join(coords)

    def get_mid_angle(start,end): return ((start+end)/2) if start<end else (((start+end+360)/2)%360)

    # --- KML文件内容生成 ---
    kml_content=f"""<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>四环-天文地理总图(V11)</name><description>从外到内:二十八宿、二十四山、十二地支、八卦。</description>"""
    # --- 样式定义 ---
    kml_content+=''.join([f'\n<Style id="style{e}"><LineStyle><width>1.2</width><color>c0ffffff</color></LineStyle><PolyStyle><color>{c}</color></PolyStyle></Style>' for e,c in element_colors.items()])
    kml_content+=''.join([f'\n<Style id="styleMountain{i}"><LineStyle><width>1</width><color>a0ffffff</color></LineStyle><PolyStyle><color>{c}</color></PolyStyle></Style>' for i,c in enumerate(mountain_colors)])
    kml_content+=''.join([f'\n<Style id="styleBranch{i}"><LineStyle><width>0.8</width><color>a0ffffff</color></LineStyle><PolyStyle><color>{c}</color></PolyStyle></Style>' for i,c in enumerate(branch_colors)])
    kml_content+=''.join([f'\n<Style id="styleGua{i}"><LineStyle><width>0.6</width><color>a0ffffff</color></LineStyle><PolyStyle><color>{c}</color></PolyStyle></Style>' for i,c in enumerate(gua_colors)])
    # MODIFIED: 将所有字体颜色改为醒目的金黄色(ff00ffff)，并保持深色光晕效果
    kml_content+="""
    <Style id="styleMansionLabel"><IconStyle><scale>0</scale></IconStyle><LabelStyle><color>ff00ffff</color><scale>0.9</scale><bgColor>b3000000</bgColor></LabelStyle></Style>
    <Style id="styleMountainLabel"><IconStyle><scale>0</scale></IconStyle><LabelStyle><color>ff00ffff</color><scale>0.75</scale><bgColor>b3000000</bgColor></LabelStyle></Style>
    <Style id="styleBranchLabel"><IconStyle><scale>0</scale></IconStyle><LabelStyle><color>ff00ffff</color><scale>0.6</scale><bgColor>b3000000</bgColor></LabelStyle></Style>
    <Style id="styleGuaLabel"><IconStyle><scale>0</scale></IconStyle><LabelStyle><color>ff00ffff</color><scale>0.8</scale><bgColor>b3000000</bgColor></LabelStyle></Style>
    <Style id="styleAngleLabel"><IconStyle><scale>0</scale></IconStyle><LabelStyle><color>ff00ffff</color><scale>1.0</scale><bgColor>b3000000</bgColor></LabelStyle></Style>
    <Style id="styleCrosshair"><LineStyle><color>ffffffff</color><width>1.5</width></LineStyle></Style>"""

    # --- 创建KML文件夹和Placemarks ---
    def create_ring_placemarks(folder_name,data,r_outer,r_inner,label_style,style_map_func):
        folder_content=f"\n<Folder><name>{folder_name}</name>"
        for i,(item_name,start,end) in enumerate(data):
            style_url,placemark_name,label_text=style_map_func(i,item_name)
            coords=create_ring_segment_coords(center_lat,center_lon,r_outer,r_inner,start,end)
            folder_content+=f'<Placemark><name>{placemark_name}</name><styleUrl>{style_url}</styleUrl><Polygon><altitudeMode>clampToGround</altitudeMode><outerBoundaryIs><LinearRing><coordinates>{coords}</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'
            mid=get_mid_angle(start,end)
            lat,lon=get_destination_point(center_lat,center_lon,mid,(r_outer+r_inner)/2)
            folder_content+=f'<Placemark><name>{label_text}</name><styleUrl>#{label_style}</styleUrl><Point><coordinates>{lon},{lat},0</coordinates></Point></Placemark>'
        folder_content+="\n</Folder>"
        return folder_content
    
    kml_content+=create_ring_placemarks("环1：二十八宿",mansions_data,r1_outer_m,r1_inner_m,"styleMansionLabel",lambda i,name:(f"#style{'火' if elements_map.get(name,'') in ['日','月'] else elements_map.get(name,'')}",f"{name} ({elements_map.get(name,'')})",f"{name}\n({elements_map.get(name,'')})"))
    kml_content+=create_ring_placemarks("环2：二十四山",mountains_data,r2_outer_m,r2_inner_m,"styleMountainLabel",lambda i,name:(f"#styleMountain{i%len(mountain_colors)}",name,name))
    kml_content+=create_ring_placemarks("环3：十二地支",branches_data,r3_outer_m,r3_inner_m,"styleBranchLabel",lambda i,name:(f"#styleBranch{i%len(branch_colors)}",name,name))
    kml_content+=create_ring_placemarks("环4：八卦",gua_data,r4_outer_m,r4_inner_m,"styleGuaLabel",lambda i,name:(f"#styleGua{i%len(gua_colors)}",name,name))
    
    # 中心与外部标记
    kml_content += "\n<Folder><name>中心与外部标记</name>"
    if r4_inner_m>0:
        cross_r=r4_inner_m*0.9
        lat_n,lon_n=get_destination_point(center_lat,center_lon,0,cross_r);lat_s,lon_s=get_destination_point(center_lat,center_lon,180,cross_r)
        lat_e,lon_e=get_destination_point(center_lat,center_lon,90,cross_r);lat_w,lon_w=get_destination_point(center_lat,center_lon,270,cross_r)
        kml_content+=f'<Placemark><name>中心十字</name><styleUrl>#styleCrosshair</styleUrl><MultiGeometry><LineString><coordinates>{lon_n},{lat_n},0 {lon_s},{lat_s},0</coordinates></LineString><LineString><coordinates>{lon_e},{lat_e},0 {lon_w},{lat_w},0</coordinates></LineString></MultiGeometry></Placemark>'
    for angle in range(0,360,15):
        lat,lon=get_destination_point(center_lat,center_lon,angle,r1_outer_m*1.15)
        kml_content+=f'<Placemark><name>{angle}°</name><styleUrl>#styleAngleLabel</styleUrl><Point><coordinates>{lon},{lat},0</coordinates></Point></Placemark>'
    kml_content += "\n</Folder>"

    kml_content += """\n</Document>\n</kml>"""
    try:
        with open(file_name,'w',encoding='utf-8') as f: f.write(kml_content)
        print(f"成功！文件 '{file_name}' 已在当前目录生成。"); print(f"配置: 中心=({center_lat},{center_lon}), 外环半径={r1_outer_m}米")
    except Exception as e: print(f"错误：无法写入文件。 {e}")

# ==============================================================================
# 3. 运行主程序
# ==============================================================================
if __name__ == "__main__":
    create_kml_ultimate_map(
        center_lat=CENTER_LATITUDE,
        center_lon=CENTER_LONGITUDE,
        r1_outer_m=RING_1_OUTER_RADIUS_METERS,
        r1_thick_pct=RING_1_THICKNESS_PERCENT,
        gap12_pct=GAP_1_2_PERCENT,
        r2_thick_pct=RING_2_THICKNESS_PERCENT,
        gap23_pct=GAP_2_3_PERCENT,
        r3_thick_pct=RING_3_THICKNESS_PERCENT,
        gap34_pct=GAP_3_4_PERCENT,
        r4_thick_pct=RING_4_THICKNESS_PERCENT,
        file_name=OUTPUT_KML_FILE
    )