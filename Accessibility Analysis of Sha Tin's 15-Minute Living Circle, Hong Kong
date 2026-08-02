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

# ========== 中文字体配置 ==========
def get_chinese_font():
    font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    chinese_fonts_keywords = ['SimHei', 'Microsoft YaHei', 'Heiti', 'STHeiti', 'Noto Sans CJK', 'PingFang', 'WenQuanYi']
    for font_path in font_list:
        font_name = fm.FontProperties(fname=font_path).get_name()
        if any(keyword.lower() in font_name.lower() for keyword in chinese_fonts_keywords):
            return font_name
    return 'sans-serif'

system_font = get_chinese_font()
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = [system_font, 'SimHei', 'Microsoft YaHei', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

print(f"✓ 字体配置完成，当前使用字体: {system_font}")
print("=" * 80)

# --- 1. 配置路径 ---
DATA_PATH = "./data"
boundary_geojson = f"{DATA_PATH}/boundary.geojson"
population_csv = f"{DATA_PATH}/boundary.CSV"
bus_file = f"{DATA_PATH}/bus.geojson"
park_file = f"{DATA_PATH}/parks.geojson"
hospital_file = f"{DATA_PATH}/hospitals.geojson"

# --- 2. 加载数据 ---
print("开始加载数据...")
print("-" * 60)

# 2.1 加载边界地理数据
try:
    boundary_gdf = gpd.read_file(boundary_geojson)
    print(f"✓ 边界地理数据加载成功: {len(boundary_gdf)} 个区域")
    print(f"  可用列: {boundary_gdf.columns.tolist()}")
except Exception as e:
    print(f"✗ 加载边界地理数据失败: {e}")
    exit()

# 2.2 加载人口统计数据
try:
    population_df = pd.read_csv(population_csv, skiprows=3, encoding='utf-8-sig')
    population_df.columns = population_df.columns.str.strip()
    print(f"✓ 人口统计数据加载成功: {len(population_df)} 条记录")
    print(f"  可用列: {population_df.columns.tolist()}")
except Exception as e:
    print(f"✗ 加载人口统计数据失败: {e}")
    population_df = pd.DataFrame()

# 2.3 加载设施数据
try:
    bus_stops = gpd.read_file(bus_file)
    print(f"✓ 巴士站数据加载成功: {len(bus_stops)} 个站点")
except Exception as e:
    print(f"✗ 加载巴士站数据失败: {e}")
    bus_stops = gpd.GeoDataFrame()

try:
    parks = gpd.read_file(park_file)
    print(f"✓ 公园数据加载成功: {len(parks)} 个公园")
except Exception as e:
    print(f"✗ 加载公园数据失败: {e}")
    parks = gpd.GeoDataFrame()

try:
    hospitals = gpd.read_file(hospital_file)
    print(f"✓ 医院数据加载成功: {len(hospitals)} 个医院/诊所")
except Exception as e:
    print(f"✗ 加载医院数据失败: {e}")
    hospitals = gpd.GeoDataFrame()

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

# 3.2 提取沙田区边界
print("\n正在提取沙田区边界...")
sha_tin_gdf = None
sha_tin_name = None

# 尝试多种可能的沙田区名称
possible_names = ['沙田', '沙田区', 'Sha Tin', 'Sha Tin District']
for col in boundary_gdf.columns:
    for name in possible_names:
        if name in boundary_gdf[col].astype(str).values:
            sha_tin_gdf = boundary_gdf[boundary_gdf[col].astype(str).str.contains(name, na=False)]
            sha_tin_name = name
            break
    if sha_tin_gdf is not None:
        break

if sha_tin_gdf is None or sha_tin_gdf.empty:
    # 如果无法通过名称匹配，尝试通过经纬度范围
    print("⚠ 无法通过名称匹配沙田区，尝试通过经纬度范围...")
    # 沙田区大致经纬度范围
    min_lon, max_lon = 114.1, 114.3
    min_lat, max_lat = 22.3, 22.45
    bbox = box(min_lon, min_lat, max_lon, max_lat)
    sha_tin_gdf = boundary_gdf[boundary_gdf.intersects(bbox)]
    if not sha_tin_gdf.empty:
        print(f"✓ 通过经纬度范围找到 {len(sha_tin_gdf)} 个区域")
    else:
        # 如果还是找不到，使用第一个区域（可能数据本身就是沙田区）
        print("⚠ 使用整个边界数据（可能数据本身是沙田区）")
        sha_tin_gdf = boundary_gdf

print(f"✓ 沙田区边界提取完成，共 {len(sha_tin_gdf)} 个多边形")
if 'dcca_chi' in sha_tin_gdf.columns:
    print(f"  区域名称: {sha_tin_gdf['dcca_chi'].values}")

# 3.3 合并人口数据
print("\n合并人口数据...")
if not population_df.empty and 'dcca_chi' in boundary_gdf.columns:
    # 尝试匹配人口数据
    merge_key = None
    for col in ['dcca_chi', 'dcca_eng', 'dc_chi', 'ca_chi']:
        if col in boundary_gdf.columns and col in population_df.columns:
            merge_key = col
            break
    
    if merge_key:
        boundary_gdf[merge_key] = boundary_gdf[merge_key].astype(str).str.strip()
        population_df[merge_key] = population_df[merge_key].astype(str).str.strip()
        boundary_gdf = boundary_gdf.merge(population_df, on=merge_key, how='left')
        print(f"  ✓ 通过 '{merge_key}' 匹配人口数据")
    else:
        print("  ⚠ 无法匹配人口数据，使用默认值")
        boundary_gdf['t_pop'] = 10000
        boundary_gdf['elder_pop'] = 1500
else:
    print("  ⚠ 人口数据为空或列名不匹配")
    boundary_gdf['t_pop'] = 10000
    boundary_gdf['elder_pop'] = 1500

# 3.4 标准化设施数据
def prepare_facilities(gdf, facility_type):
    if gdf.empty:
        return gdf
    
    gdf = gdf.copy()
    gdf['facility_type'] = facility_type
    
    # 提取名称
    name_cols = ['name', 'Name', 'NAME', 'facility_name', 'stop_name', 'park_name', 'hospital_name']
    for col in name_cols:
        if col in gdf.columns:
            gdf['facility_name'] = gdf[col]
            break
    if 'facility_name' not in gdf.columns:
        gdf['facility_name'] = gdf.index.astype(str)
    
    # 提取服务时间
    time_cols = ['service_time', 'service_hours', 'opening_hours']
    for col in time_cols:
        if col in gdf.columns:
            gdf['service_time'] = gdf[col]
            break
    if 'service_time' not in gdf.columns:
        gdf['service_time'] = '未知'
    
    # 获取经纬度
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

# 4.2 创建沙田区的网格分析
print("正在创建分析网格...")
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

# 4.3 计算每个网格点的15分钟可达设施
print("正在计算设施可达性...")
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

# --- 7. 可视化 ---
print("\n" + "=" * 80)
print("生成可视化图表...")
print("=" * 80)

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 图1: 设施覆盖热力图
ax1 = axes[0, 0]
grid_gdf.plot(column='total_facilities', ax=ax1, cmap='YlOrRd', 
              markersize=20, legend=True, edgecolor='none',
              legend_kwds={'label': '15分钟可达设施数', 'shrink': 0.6})
sha_tin_proj.boundary.plot(ax=ax1, color='blue', linewidth=2, label='沙田区边界')
if not facilities_proj.empty:
    facilities_proj.plot(ax=ax1, color='green', markersize=3, alpha=0.3, label='设施')
ax1.set_title('沙田区15分钟生活圈设施覆盖', fontsize=12, fontweight='bold')
ax1.axis('off')
ax1.legend(loc='lower right')

# 图2: 15分钟生活圈达标情况
ax2 = axes[0, 1]
grid_gdf.plot(column='is_well_served', ax=ax2, categorical=True, 
              cmap='RdYlGn_r', markersize=20, legend=True, edgecolor='none')
sha_tin_proj.boundary.plot(ax=ax2, color='black', linewidth=2)
ax2.set_title('15分钟生活圈达标情况\n(绿色=达标, 红色=不达标)', fontsize=12, fontweight='bold')
ax2.axis('off')

# 图3: 设施等级分布
ax3 = axes[0, 2]
grid_gdf.plot(column='facility_level', ax=ax3, categorical=True, 
              cmap='RdYlGn', markersize=20, legend=True, edgecolor='none')
sha_tin_proj.boundary.plot(ax=ax3, color='black', linewidth=2)
ax3.set_title('设施等级分布', fontsize=12, fontweight='bold')
ax3.axis('off')

# 图4: 各类设施分布
ax4 = axes[1, 0]
type_colors = {'bus_stop': '#2E86AB', 'park': '#4CAF50', 'hospital': '#E74C3C'}
type_labels = {'bus_stop': '巴士站', 'park': '公园', 'hospital': '医院'}

if not facilities_proj.empty:
    for ftype, color in type_colors.items():
        subset = facilities_proj[facilities_proj['facility_type'] == ftype]
        if not subset.empty:
            subset.plot(ax=ax4, color=color, markersize=10, 
                       label=type_labels.get(ftype, ftype), alpha=0.7, edgecolor='black')
sha_tin_proj.boundary.plot(ax=ax4, color='black', linewidth=2)
ax4.set_title('沙田区各类设施分布', fontsize=12, fontweight='bold')
ax4.axis('off')
ax4.legend()

# 图5: 服务不足区域统计
ax5 = axes[1, 1]
if not underserved.empty:
    # 绘制服务不足区域
    underserved.plot(ax=ax5, color='red', markersize=25, alpha=0.7, label='服务不足')
    sha_tin_proj.boundary.plot(ax=ax5, color='black', linewidth=2)
    ax5.set_title(f'服务不足区域\n(共{len(underserved)}个网格点)', fontsize=12, fontweight='bold')
else:
    ax5.text(0.5, 0.5, '所有区域服务良好！', ha='center', va='center', 
             transform=ax5.transAxes, fontsize=16, color='green')
ax5.axis('off')
if not underserved.empty:
    ax5.legend()

# 图6: 统计图表
ax6 = axes[1, 2]
if not underserved.empty:
    # 显示设施缺失类型统计
    missing_stats = {
        '缺少巴士站': len(underserved[underserved['bus_stops'] == 0]),
        '缺少公园': len(underserved[underserved['parks'] == 0]),
        '缺少医院': len(underserved[underserved['hospitals'] == 0])
    }
    bars = ax6.bar(missing_stats.keys(), missing_stats.values(), color=['#2E86AB', '#4CAF50', '#E74C3C'])
    ax6.set_title('服务不足区域\n设施缺失类型', fontsize=12, fontweight='bold')
    ax6.set_ylabel('网格点数量', fontsize=10)
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')
else:
    ax6.text(0.5, 0.5, '所有区域设施覆盖良好！', ha='center', va='center', 
             transform=ax6.transAxes, fontsize=14, color='green')

plt.tight_layout()
plt.savefig('sha_tin_15min_living_circle.png', dpi=300, bbox_inches='tight')
print("✓ 图表已保存为 'sha_tin_15min_living_circle.png'")
plt.show()

# --- 8. 导出详细结果 ---
print("\n" + "=" * 80)
print("导出分析结果...")
print("=" * 80)

# 8.1 导出网格分析结果
grid_export = grid_gdf.to_crs("EPSG:4326")
grid_export.to_file('sha_tin_15min_analysis.geojson', driver='GeoJSON')
print("✓ 网格分析结果已导出为 'sha_tin_15min_analysis.geojson'")

# 8.2 导出服务不足区域
if not underserved.empty:
    underserved_export = underserved.to_crs("EPSG:4326")
    underserved_export.to_file('sha_tin_underserved_areas.geojson', driver='GeoJSON')
    print("✓ 服务不足区域已导出为 'sha_tin_underserved_areas.geojson'")

# 8.3 导出统计摘要CSV
summary_stats = {
    '指标': ['总网格点数', '达标网格点数', '达标率', '平均设施数', '平均巴士站数', '平均公园数', '平均医院数'],
    '数值': [
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
print("✓ 统计摘要已导出为 'sha_tin_analysis_summary.csv'")

# 8.4 导出设施列表
if not facilities_gdf.empty:
    facilities_export = facilities_gdf.to_crs("EPSG:4326")
    facilities_export.to_file('sha_tin_facilities.geojson', driver='GeoJSON')
    print("✓ 设施列表已导出为 'sha_tin_facilities.geojson'")

# 8.5 导出服务不足区域详细报告
if not underserved.empty:
    underserved_detail = underserved.copy()
    underserved_detail['nearest_facilities'] = underserved_detail['facility_names']
    underserved_detail = underserved_detail.to_crs("EPSG:4326")
    
    detail_cols = ['x', 'y', 'total_facilities', 'bus_stops', 'parks', 'hospitals', 'facility_names']
    available_cols = [col for col in detail_cols if col in underserved_detail.columns]
    underserved_detail[available_cols].to_csv('sha_tin_underserved_detail.csv', index=False, encoding='utf-8-sig')
    print("✓ 服务不足区域详细报告已导出为 'sha_tin_underserved_detail.csv'")

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
