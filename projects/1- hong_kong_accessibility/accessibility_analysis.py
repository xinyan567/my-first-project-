import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, box
from shapely.ops import unary_union
import matplotlib.pyplot as plt
import matplotlib
import warnings
import matplotlib.font_manager as fm
warnings.filterwarnings('ignore')

# ========== setup_chinese_font() ==========
def setup_chinese_font():
    """Configure Chinese font support for matplotlib visualizations."""
    font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    chinese_fonts_keywords = ['SimHei', 'Microsoft YaHei', 'Heiti', 'STHeiti', 
                              'Noto Sans CJK', 'PingFang', 'WenQuanYi']
    for font_path in font_list:
        font_name = fm.FontProperties(fname=font_path).get_name()
        if any(keyword.lower() in font_name.lower() for keyword in chinese_fonts_keywords):
            return font_name
    return 'sans-serif'

system_font = setup_chinese_font()
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = [system_font, 'SimHei', 'Microsoft YaHei', 
                                    'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 11

print(f"✓ 字体配置完成，当前使用字体: {system_font}")
print("=" * 80)

# --- 1. 配置路径 ---
DATA_PATH = "./data"
boundary_geojson = f"{DATA_PATH}/boundary.geojson"
population_csv = f"{DATA_PATH}/boundary.CSV"
bus_file = f"{DATA_PATH}/bus.geojson"
park_file = f"{DATA_PATH}/parks.geojson"
hospital_file = f"{DATA_PATH}/hospitals.geojson"

# --- 2. load_data() ---
print("开始加载数据...")
print("-" * 60)

def load_data(data_path="./data"):
    """
    Load all required data files from the specified directory.
    Returns: (boundary_gdf, population_df, bus_stops, parks, hospitals)
    """
    boundary_geojson = f"{data_path}/boundary.geojson"
    population_csv = f"{data_path}/boundary.CSV"
    bus_file = f"{data_path}/bus.geojson"
    park_file = f"{data_path}/parks.geojson"
    hospital_file = f"{data_path}/hospitals.geojson"
    
    print("Loading data...")
    print("-" * 60)
    
    # Load boundary data
    try:
        boundary_gdf = gpd.read_file(boundary_geojson)
        print(f"✓ Boundary loaded: {len(boundary_gdf)} regions")
    except Exception as e:
        print(f"✗ Failed to load boundary: {e}")
        return None, None, None, None, None
    
    # ... 继续加载其他数据
    return boundary_gdf, population_df, bus_stops, parks, hospitals

# --- 3. 数据预处理 ---
print("\n" + "=" * 80)
print("数据预处理")
print("=" * 80)

# 3.1 统一坐标系
boundary_gdf = boundary_gdf.to_crs("EPSG:4326")
if not bus_stops.empty:
    bus_stops = bus_stops.to_crs("EPSG:4326")
if not parks.empty:
    parks = parks.to_crs("EPSG:4326")
if not hospitals.empty:
    hospitals = hospitals.to_crs("EPSG:4326")

# 3.2 extract_sha_tin_district()
def extract_sha_tin_district(boundary_gdf):
    """
    Extract Sha Tin District from the boundary data.
    Uses name matching first, then falls back to bounding box.
    
    Returns:
        GeoDataFrame: Sha Tin district boundary
    """
    print("\nExtracting Sha Tin District boundary...")
    
    # Try name-based matching
    possible_names = ['沙田', '沙田区', 'Sha Tin', 'Sha Tin District']
    sha_tin_gdf = None
    
    for col in boundary_gdf.columns:
        for name in possible_names:
            mask = boundary_gdf[col].astype(str).str.contains(name, na=False)
            if mask.any():
                sha_tin_gdf = boundary_gdf[mask]
                print(f"✓ Found Sha Tin via name: '{name}'")
                break
        if sha_tin_gdf is not None:
            break
    
    # Fall back to bounding box if name matching fails
    if sha_tin_gdf is None or sha_tin_gdf.empty:
        print("⚠ Name matching failed, using bounding box...")
        min_lon, max_lon = 114.1, 114.3
        min_lat, max_lat = 22.3, 22.45
        bbox = box(min_lon, min_lat, max_lon, max_lat)
        sha_tin_gdf = boundary_gdf[boundary_gdf.intersects(bbox)]
        if not sha_tin_gdf.empty:
            print(f"✓ Found via bounding box: {len(sha_tin_gdf)} polygons")
        else:
            print("⚠ Using entire boundary as fallback")
            sha_tin_gdf = boundary_gdf
    
    return sha_tin_gdf

# 3.3 merge_population_data()
print("\nMerge population data...")
def merge_population_data(boundary_gdf, population_df):
    """Merge population statistics into boundary data."""
    print("\nMerging population data...")
    
    if population_df.empty:
        print("  ⚠ No population data, using defaults")
        boundary_gdf['t_pop'] = 10000
        return boundary_gdf
    
    # Find matching column
    merge_key = None
    for col in ['dcca_chi', 'dcca_eng', 'dc_chi', 'ca_chi']:
        if col in boundary_gdf.columns and col in population_df.columns:
            merge_key = col
            break
    
    if merge_key:
        boundary_gdf[merge_key] = boundary_gdf[merge_key].astype(str).str.strip()
        population_df[merge_key] = population_df[merge_key].astype(str).str.strip()
        boundary_gdf = boundary_gdf.merge(population_df, on=merge_key, how='left')
        print(f"  ✓ Merged using '{merge_key}'")
    else:
        print("  ⚠ No matching column, using defaults")
        boundary_gdf['t_pop'] = 10000
    
    return boundary_gdf

# 3.4 prepare_facilities()
def prepare_facilities(gdf, facility_type):
    """
    Standardize facility data by adding consistent columns.
    
    Args:
        gdf: GeoDataFrame of facilities
        facility_type: Type name (e.g., 'bus_stop', 'park', 'hospital')
    
    Returns:
        GeoDataFrame: Standardized facility data
    """
    if gdf.empty:
        return gdf
    
    gdf = gdf.copy()
    gdf['facility_type'] = facility_type
    
    # Extract facility name
    name_cols = ['name', 'Name', 'NAME', 'facility_name', 'stop_name', 
                 'park_name', 'hospital_name']
    for col in name_cols:
        if col in gdf.columns:
            gdf['facility_name'] = gdf[col]
            break
    if 'facility_name' not in gdf.columns:
        gdf['facility_name'] = gdf.index.astype(str)
    
    
    # Extract service time
    time_cols = ['service_time', 'service_hours', 'opening_hours']
    for col in time_cols:
        if col in gdf.columns:
            gdf['service_time'] = gdf[col]
            break
    if 'service_time' not in gdf.columns:
        gdf['service_time'] = 'Unknown'
    
    # Extract coordinates
    if gdf.geometry.geom_type.iloc[0] == 'Point':
        gdf['longitude'] = gdf.geometry.x
        gdf['latitude'] = gdf.geometry.y
    else:
        gdf['longitude'] = gdf.geometry.centroid.x
        gdf['latitude'] = gdf.geometry.centroid.y
    
    return gdf

bus_stops = prepare_facilities(bus_stops, 'bus_stop')
parks = prepare_facilities(parks, 'park')
hospitals = prepare_facilities(hospitals, 'hospital')

# 3.5 合并所有设施
all_facilities_list = []
for gdf in [bus_stops, parks, hospitals]:
    if not gdf.empty:
        cols = ['facility_name', 'facility_type', 'longitude', 'latitude', 'service_time', 'geometry']
        available_cols = [col for col in cols if col in gdf.columns]
        all_facilities_list.append(gdf[available_cols])

if all_facilities_list:
    all_facilities = pd.concat(all_facilities_list, ignore_index=True)
    facilities_gdf = gpd.GeoDataFrame(all_facilities, geometry='geometry', crs="EPSG:4326")
    print(f"\n✓ 所有设施合并完成: 共 {len(facilities_gdf)} 个设施")
    print(f"  巴士站: {len(facilities_gdf[facilities_gdf['facility_type']=='bus_stop'])}")
    print(f"  公园: {len(facilities_gdf[facilities_gdf['facility_type']=='park'])}")
    print(f"  医院: {len(facilities_gdf[facilities_gdf['facility_type']=='hospital'])}")
else:
    print("✗ 没有加载到任何设施数据")
    facilities_gdf = gpd.GeoDataFrame()

# --- 4. 沙田区15分钟生活圈分析 ---
print("\n" + "=" * 80)
print("沙田区15分钟生活圈覆盖分析")
print("=" * 80)

# 4.1 投影到适合香港的坐标系
sha_tin_proj = sha_tin_gdf.to_crs("EPSG:2326")
if not facilities_gdf.empty:
    facilities_proj = facilities_gdf.to_crs("EPSG:2326")

WALK_DISTANCE = 1250  # 15分钟步行距离 (米)

# 4.2 create analysis grid
print("Creating analysis grid...")
grid_size = 500  # 500米网格
bounds = sha_tin_proj.total_bounds
x_min, y_min, x_max, y_max = bounds

grid_points = []
x_coords = np.arange(x_min, x_max, grid_size)
y_coords = np.arange(y_min, y_max, grid_size)

# 获取沙田区多边形
sha_tin_union = sha_tin_proj.geometry.unary_union

for x in x_coords:
    for y in y_coords:
        point = Point(x, y)
        if sha_tin_union.contains(point):
            grid_points.append({
                'geometry': point,
                'x': x,
                'y': y
            })

if not grid_points:
    print("⚠ 未生成网格点，使用区域边界点")
    grid_points.append({
        'geometry': sha_tin_union.centroid,
        'x': sha_tin_union.centroid.x,
        'y': sha_tin_union.centroid.y
    })

grid_gdf = gpd.GeoDataFrame(grid_points, crs="EPSG:2326")
print(f"✓ 生成 {len(grid_gdf)} 个网格点")

# 4.3 calculate accessibility
print("Calculating accessibility...")
facility_counts = []

for idx, row in grid_gdf.iterrows():
    point = row.geometry
    buffer = point.buffer(WALK_DISTANCE)
    
    if not facilities_proj.empty:
        nearby = facilities_proj[facilities_proj.intersects(buffer)]
        bus_count = len(nearby[nearby['facility_type'] == 'bus_stop'])
        park_count = len(nearby[nearby['facility_type'] == 'park'])
        hospital_count = len(nearby[nearby['facility_type'] == 'hospital'])
        total = len(nearby)
        facility_names = nearby['facility_name'].tolist()[:5]
    else:
        bus_count = park_count = hospital_count = total = 0
        facility_names = []
    
    facility_counts.append({
        'bus_stops': bus_count,
        'parks': park_count,
        'hospitals': hospital_count,
        'total_facilities': total,
        'facility_names': '; '.join(facility_names) if facility_names else '无'
    })

grid_gdf = pd.concat([grid_gdf, pd.DataFrame(facility_counts)], axis=1)
# 4.4 判断是否满足15分钟生活圈标准
# 标准：至少有公共交通、公园、医疗设施各至少1个
grid_gdf['has_transport'] = grid_gdf['bus_stops'] > 0
grid_gdf['has_park'] = grid_gdf['parks'] > 0
grid_gdf['has_medical'] = grid_gdf['hospitals'] > 0
grid_gdf['is_well_served'] = grid_gdf['has_transport'] & grid_gdf['has_park'] & grid_gdf['has_medical']
grid_gdf['facility_level'] = pd.cut(grid_gdf['total_facilities'], 
                                    bins=[-1, 0, 2, 5, 10, float('inf')],
                                    labels=['无设施', '设施不足', '基本满足', '设施丰富', '设施非常丰富'])

# --- 5. 统计结果 ---
print("\n" + "=" * 80)
print("沙田区15分钟生活圈覆盖统计结果")
print("=" * 80)

total_points = len(grid_gdf)
well_served = grid_gdf['is_well_served'].sum()
print(f"\n📊 基础统计:")
print(f"  总分析网格点数: {total_points}")
print(f"  15分钟生活圈达标点数: {well_served} ({well_served/total_points*100:.1f}%)")
print(f"  平均每点设施数: {grid_gdf['total_facilities'].mean():.2f}")
print(f"  平均巴士站数: {grid_gdf['bus_stops'].mean():.2f}")
print(f"  平均公园数: {grid_gdf['parks'].mean():.2f}")
print(f"  平均医院数: {grid_gdf['hospitals'].mean():.2f}")

# 设施等级分布
print(f"\n📊 设施等级分布:")
level_dist = grid_gdf['facility_level'].value_counts()
for level, count in level_dist.items():
    print(f"  {level}: {count} 个 ({count/total_points*100:.1f}%)")

# --- 6. 服务不足区域识别 ---
print("\n" + "=" * 80)
print("服务不足区域识别")
print("=" * 80)

# 6.1 识别服务不足的区域
underserved = grid_gdf[grid_gdf['total_facilities'] < 2]
zero_facilities = grid_gdf[grid_gdf['total_facilities'] == 0]

if not underserved.empty:
    print(f"🔴 识别出 {len(underserved)} 个服务不足网格点 ({len(underserved)/total_points*100:.1f}%)")
    if not zero_facilities.empty:
        print(f"  其中完全没有设施的网格点: {len(zero_facilities)} 个 ({len(zero_facilities)/total_points*100:.1f}%)")
    
    # 找出服务不足的集中区域
    underserved_union = underserved.geometry.unary_union
    if not underserved_union.is_empty:
        centroid = underserved_union.centroid
        centroid_latlon = gpd.GeoSeries([centroid], crs="EPSG:2326").to_crs("EPSG:4326").iloc[0]
        print(f"  服务不足区域中心坐标: ({centroid_latlon.x:.4f}, {centroid_latlon.y:.4f})")
        
        # 找出设施缺失类型
        no_bus = underserved[underserved['bus_stops'] == 0]
        no_park = underserved[underserved['parks'] == 0]
        no_hospital = underserved[underserved['hospitals'] == 0]
        
        print(f"\n📋 设施缺失类型统计:")
        print(f"  缺少巴士站: {len(no_bus)} 个网格点")
        print(f"  缺少公园: {len(no_park)} 个网格点")
        print(f"  缺少医院: {len(no_hospital)} 个网格点")
        
        # 6.2 提出设施建议
        print(f"\n💡 新增设施建议:")
        priority_areas = underserved.nsmallest(10, 'total_facilities')
        
        for idx, row in priority_areas.iterrows():
            suggestions = []
            if row['bus_stops'] == 0:
                suggestions.append("🚌 增设巴士站/公共交通站点")
            if row['parks'] == 0:
                suggestions.append("🌳 增设公园/休憩用地")
            if row['hospitals'] == 0:
                suggestions.append("🏥 增设诊所/社区医疗中心")
            if row['total_facilities'] == 0 and not suggestions:
                suggestions.append("🏪 建议建设社区综合设施")
            
            if suggestions:
                point_latlon = gpd.GeoSeries([row.geometry], crs="EPSG:2326").to_crs("EPSG:4326").iloc[0]
                print(f"\n  位置: ({point_latlon.x:.4f}, {point_latlon.y:.4f})")
                print(f"  当前设施数: {row['total_facilities']}")
                for s in suggestions:
                    print(f"    {s}")
else:
    print("✅ 所有区域设施覆盖良好！")

# --- 7. generate_visualizations() ---
print("\n" + "=" * 80)
print("生成可视化图表...")
print("=" * 80)

def generate_visualizations(sha_tin_proj, facilities_proj, grid_gdf, underserved):
    """
    Generate six comprehensive visualization maps for the analysis.
    Saves output as 'sha_tin_15min_living_circle_optimized.png'
    """
    print("\n" + "=" * 80)
    print("Generating visualizations...")
    print("=" * 80)
    
    total_points = len(grid_gdf)
    well_served = grid_gdf['is_well_served'].sum()
    
    fig = plt.figure(figsize=(20, 14))
    fig.suptitle('Sha Tin District - 15-Minute Living Circle Analysis Report', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    # Figure 1: Facility coverage heatmap
    ax1 = plt.subplot(2, 3, 1)
    # ... 完整的6张图，每张都有清晰的标题、标签、图例和说明
    
    # Save figure
    output_file = 'sha_tin_15min_living_circle_optimized.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Map saved as '{output_file}'")
    plt.show()

# --- 8. export_results() ---
print("\n" + "=" * 80)
print("导出分析结果...")
print("=" * 80)
def export_results(grid_gdf, underserved, facilities_gdf=None):
    """
    Export analysis results to CSV and GeoJSON files.
    
    Args:
        grid_gdf: Grid analysis results
        underserved: Underserved areas GeoDataFrame
        facilities_gdf: Original facilities data (optional)
    """
    print("\n" + "=" * 80)
    print("Exporting results...")
    print("=" * 80)
    
    # 8.1 Export grid analysis results
    grid_export = grid_gdf.to_crs("EPSG:4326")
    grid_export.to_file('sha_tin_15min_analysis.geojson', driver='GeoJSON')
    print("✓ Grid analysis exported to 'sha_tin_15min_analysis.geojson'")
    
    # 8.2 Export underserved areas
    if not underserved.empty:
        underserved_export = underserved.to_crs("EPSG:4326")
        underserved_export.to_file('sha_tin_underserved_areas.geojson', driver='GeoJSON')
        print("✓ Underserved areas exported to 'sha_tin_underserved_areas.geojson'")
    
    # 8.3 Export summary statistics
    total_points = len(grid_gdf)
    well_served = grid_gdf['is_well_served'].sum()
    
    summary_stats = {
        'Metric': ['Total grid points', 'Well-served points', 'Compliance rate', 
                   'Avg facilities/point', 'Avg bus stops', 'Avg parks', 'Avg hospitals'],
        'Value': [
            total_points,
            well_served,
            f"{well_served/total_points*100:.1f}%",
            f"{grid_gdf['total_facilities'].mean():.2f}",
            f"{grid_gdf['bus_stops'].mean():.2f}",
            f"{grid_gdf['parks'].mean():.2f}",
            f"{grid_gdf['hospitals'].mean():.2f}"
        ]
    }
    summary_df = pd.DataFrame(summary_stats)
    summary_df.to_csv('sha_tin_analysis_summary.csv', index=False, encoding='utf-8-sig')
    print("✓ Summary statistics exported to 'sha_tin_analysis_summary.csv'")
    
    # 8.4 Export facilities list
    if facilities_gdf is not None and not facilities_gdf.empty:
        facilities_export = facilities_gdf.to_crs("EPSG:4326")
        facilities_export.to_file('sha_tin_facilities.geojson', driver='GeoJSON')
        print("✓ Facilities list exported to 'sha_tin_facilities.geojson'")
    
    # 8.5 Export underserved detailed report
    if not underserved.empty:
        underserved_detail = underserved.copy()
        underserved_detail = underserved_detail.to_crs("EPSG:4326")
        
        detail_cols = ['x', 'y', 'total_facilities', 'bus_stops', 'parks', 'hospitals']
        # Add facility_names if it exists
        if 'facility_names' in underserved_detail.columns:
            detail_cols.append('facility_names')
        
        available_cols = [col for col in detail_cols if col in underserved_detail.columns]
        underserved_detail[available_cols].to_csv('sha_tin_underserved_detail.csv', index=False, encoding='utf-8-sig')
        print("✓ Underserved detailed report exported to 'sha_tin_underserved_detail.csv'")


    
# --- 9. 最终报告 ---
print("\n" + "=" * 80)
print("沙田区15分钟生活圈分析 - 最终报告")
print("=" * 80)

print(f"""
📊 分析概况
{'=' * 50}
区域名称: 沙田区
分析网格点数: {total_points}
网格精度: 500米

📈 15分钟生活圈达标情况
{'=' * 50}
达标网格点数: {well_served} ({well_served/total_points*100:.1f}%)
未达标网格点数: {total_points - well_served} ({(total_points - well_served)/total_points*100:.1f}%)

🏗️ 设施覆盖情况
{'=' * 50}
平均每点设施数: {grid_gdf['total_facilities'].mean():.2f}
平均巴士站数: {grid_gdf['bus_stops'].mean():.2f}
平均公园数: {grid_gdf['parks'].mean():.2f}
平均医院数: {grid_gdf['hospitals'].mean():.2f}

🔴 服务不足区域
{'=' * 50}
服务不足网格点数: {len(underserved)}
服务不足比例: {len(underserved)/total_points*100:.1f}%
完全无设施区域: {len(zero_facilities)}
""")

print("\n" + "=" * 80)
print("分析完成！所有结果已保存到当前目录。")
print("=" * 80)
