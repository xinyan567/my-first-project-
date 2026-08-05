# ======================================================
# 香港建筑密度与网格温度情景模拟
# ======================================================

import os
import glob
import logging
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import box
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class Config:
    PROJECT_ROOT = Path("/home/7abdebb0-f530-4878-bea4-9162061e9ca7/HK_UrbanHeat_Project")
    BUILDING_DIR = PROJECT_ROOT / "building"
    OUTPUT_DIR = PROJECT_ROOT / "outputs"
    FIGURE_DIR = OUTPUT_DIR / "figures"
    CELL_SIZE = 1000
    UHI_COEFFICIENT = 6.0
    BASE_TEMP = 17.5
    RANDOM_SEED = 42
    
    @classmethod
    def ensure_dirs(cls):
        for d in [cls.BUILDING_DIR, cls.OUTPUT_DIR, cls.FIGURE_DIR]:
            d.mkdir(parents=True, exist_ok=True)
        return cls


def read_building_data(building_dir: Path):
    """读取建筑几何数据（只读几何，跳过DBF）"""
    logger.info("\n【1】读取建筑数据...")
    
    import fiona
    from shapely.geometry import shape
    
    shp_files = glob.glob(str(building_dir / "*.shp"))
    if not shp_files:
        raise FileNotFoundError(f"未找到SHP文件")
    
    # 优先使用 Building_converted.shp
    selected_file = None
    for f in shp_files:
        if 'Building_converted' in f and 'WorksHistory' not in f:
            selected_file = f
            break
    if selected_file is None:
        selected_file = shp_files[0]
    
    logger.info(f"  使用: {Path(selected_file).name}")
    
    with fiona.open(selected_file, 'r') as src:
        logger.info(f"  几何类型: {src.schema['geometry']}")
        geometries = []
        for record in src:
            if record['geometry'] is not None:
                geometries.append(shape(record['geometry']))
        
        building = gpd.GeoDataFrame({'geometry': geometries}, crs=src.crs)
    
    # 处理坐标系
    if building.crs is None:
        bounds = building.total_bounds
        if bounds[0] > 100 and bounds[0] < 130 and bounds[1] > 20 and bounds[1] < 30:
            building = building.set_crs("EPSG:4326").to_crs("EPSG:2326")
        else:
            building = building.set_crs("EPSG:2326", allow_override=True)
    
    building['area'] = building.geometry.area
    building = building[building['area'] >= 1]
    
    logger.info(f"  ✅ 加载 {len(building)} 栋建筑")
    return building


def create_study_boundary(buildings):
    """创建研究区边界"""
    logger.info("\n【2】创建研究区边界...")
    bounds = buildings.total_bounds
    x_range = bounds[2] - bounds[0]
    y_range = bounds[3] - bounds[1]
    padding_x = max(x_range * 0.1, 1000)
    padding_y = max(y_range * 0.1, 1000)
    boundary = box(bounds[0]-padding_x, bounds[1]-padding_y, 
                   bounds[2]+padding_x, bounds[3]+padding_y)
    return gpd.GeoDataFrame({'geometry': [boundary]}, crs=buildings.crs)


def create_grid(boundary, cell_size=1000):
    """创建网格"""
    logger.info("\n【3】创建分析网格...")
    bounds = boundary.total_bounds
    grid_cells = []
    x_min = np.floor(bounds[0] / cell_size) * cell_size
    y_min = np.floor(bounds[1] / cell_size) * cell_size
    x_max = np.ceil(bounds[2] / cell_size) * cell_size
    y_max = np.ceil(bounds[3] / cell_size) * cell_size
    
    x = x_min
    while x < x_max:
        y = y_min
        while y < y_max:
            grid_cells.append(box(x, y, x + cell_size, y + cell_size))
            y += cell_size
        x += cell_size
    
    grid = gpd.GeoDataFrame({'geometry': grid_cells}, crs="EPSG:2326")
    grid = gpd.clip(grid, boundary)
    grid['cell_id'] = range(len(grid))
    grid['area_m2'] = grid.geometry.area
    logger.info(f"  ✅ 创建 {len(grid)} 个网格")
    return grid


def calculate_building_density(buildings, grid):
    """计算建筑覆盖率"""
    logger.info("\n【4】计算建筑覆盖率...")
    
    buildings_valid = buildings[buildings['area'] > 0].copy()
    if len(buildings_valid) == 0:
        grid['coverage_ratio'] = 0
        return grid
    
    joined = gpd.sjoin(buildings_valid, grid, how='inner', predicate='intersects')
    if len(joined) == 0:
        grid['coverage_ratio'] = 0
        return grid
    
    intersection_data = []
    for idx, row in joined.iterrows():
        grid_idx = row['index_right']
        grid_geom = grid.loc[grid_idx, 'geometry']
        try:
            intersection = row.geometry.intersection(grid_geom)
            if not intersection.is_empty:
                intersection_data.append({
                    'cell_id': grid_idx,
                    'intersect_area': intersection.area
                })
        except:
            continue
    
    if not intersection_data:
        grid['coverage_ratio'] = 0
        return grid
    
    inter_df = pd.DataFrame(intersection_data)
    footprint = inter_df.groupby('cell_id')['intersect_area'].sum().reset_index()
    footprint.columns = ['cell_id', 'building_footprint']
    
    grid = grid.merge(footprint, on='cell_id', how='left')
    grid['building_footprint'] = grid['building_footprint'].fillna(0)
    grid['coverage_ratio'] = (grid['building_footprint'] / grid['area_m2']).clip(0, 1)
    
    logger.info(f"  ✅ 覆盖率范围: {grid['coverage_ratio'].min():.4f} ~ {grid['coverage_ratio'].max():.4f}")
    logger.info(f"     有建筑的网格: {(grid['coverage_ratio'] > 0).sum()} 个")
    return grid


def simulate_temperature(grid_data):
    """温度情景模拟"""
    logger.info("\n【5】温度情景模拟...")
    
    np.random.seed(Config.RANDOM_SEED)
    grid_data['uhi_intensity'] = grid_data['coverage_ratio'] * Config.UHI_COEFFICIENT
    noise = np.random.normal(0, 0.08, size=len(grid_data))
    grid_data['simulated_temp'] = Config.BASE_TEMP + grid_data['uhi_intensity'] + noise
    
    logger.info(f"  ✅ 模拟温度范围: {grid_data['simulated_temp'].min():.2f}°C ~ {grid_data['simulated_temp'].max():.2f}°C")
    return grid_data


def plot_results(grid_data, output_dir):
    """生成图表"""
    logger.info("\n【6】生成分析图表...")
    
    # ===== 图1：散点图 =====
    logger.info("  生成图1：建筑覆盖率 vs 模拟温度...")
    
    # 筛选有建筑的数据
    plot_data = grid_data[grid_data['coverage_ratio'] > 0].copy()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if len(plot_data) > 0:
        ax.scatter(plot_data['coverage_ratio'], plot_data['simulated_temp'],
                   alpha=0.4, color='steelblue', s=15)
        
        if len(plot_data) > 1:
            z = np.polyfit(plot_data['coverage_ratio'], plot_data['simulated_temp'], 1)
            p = np.poly1d(z)
            r2 = np.corrcoef(plot_data['coverage_ratio'], plot_data['simulated_temp'])[0, 1]**2
            x_line = np.linspace(plot_data['coverage_ratio'].min(), plot_data['coverage_ratio'].max(), 100)
            ax.plot(x_line, p(x_line), color='#d62728', linestyle='--', 
                    linewidth=2, label=f'趋势线 (R² = {r2:.4f})')
            ax.legend()
        
        ax.set_xlim(0, plot_data['coverage_ratio'].max() * 1.1)
        
        # 【关键】添加统计信息到图表
        ax.text(0.02, 0.95, f'数据点: {len(plot_data)} 个\n覆盖率范围: {plot_data["coverage_ratio"].min():.4f} ~ {plot_data["coverage_ratio"].max():.4f}',
                transform=ax.transAxes, fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    else:
        ax.text(0.5, 0.5, '无数据', ha='center', va='center', transform=ax.transAxes, fontsize=14)
    
    ax.set_xlabel('建筑覆盖率 (Building Coverage Ratio)', fontsize=12)
    ax.set_ylabel('模拟温度 (Simulated Temperature °C)', fontsize=12)
    ax.set_title('图1：建筑覆盖率与模拟温度的关系\n(情景模拟)', fontsize=14)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # 强制覆盖保存
    plt.savefig(output_dir / 'fig1_coverage_vs_temperature.png', dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"    已更新: fig1_coverage_vs_temperature.png")
    
    # ===== 图2：箱线图 =====
    logger.info("  生成图2：高低密度区域温度对比...")
    
    if len(plot_data) >= 20:
        high = plot_data[plot_data['coverage_ratio'] > plot_data['coverage_ratio'].quantile(0.75)]
        low = plot_data[plot_data['coverage_ratio'] <= plot_data['coverage_ratio'].quantile(0.25)]
        
        fig, ax = plt.subplots(figsize=(7, 6))
        ax.boxplot([low['simulated_temp'], high['simulated_temp']],
                   tick_labels=['低密度', '高密度'],
                   patch_artist=True,
                   boxprops=dict(facecolor='lightblue', edgecolor='#1a1a1a'),
                   medianprops=dict(color='red', linewidth=2))
        ax.set_ylabel('模拟温度 (°C)', fontsize=12)
        ax.set_title('图2：高低密度区域温度对比\n(情景模拟)', fontsize=14)
        ax.grid(True, axis='y', alpha=0.3)
        
        temp_diff = high['simulated_temp'].mean() - low['simulated_temp'].mean()
        ax.text(0.02, 0.98, f'温差: {temp_diff:.2f}°C\n高密度: n={len(high)}\n低密度: n={len(low)}',
                transform=ax.transAxes, fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(output_dir / 'fig2_density_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"    已更新: fig2_density_comparison.png")
    
    # ===== 图3：空间分布 =====
    logger.info("  生成图3：模拟温度空间分布...")
    
    fig, ax = plt.subplots(figsize=(10, 8))
    grid_data.plot(column='simulated_temp', ax=ax, 
                   cmap='RdYlBu_r', edgecolor='none',
                   legend=True, legend_kwds={'label': '模拟温度 (°C)', 'shrink': 0.7})
    ax.set_title('图3：模拟温度空间分布\n(情景模拟)', fontsize=14)
    ax.set_xlabel('东向坐标 (m)', fontsize=12)
    ax.set_ylabel('北向坐标 (m)', fontsize=12)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'fig3_temperature_spatial.png', dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"    已更新: fig3_temperature_spatial.png")


def print_statistics(grid_data):
    """输出统计"""
    logger.info("\n【7】统计摘要")
    logger.info("="*60)
    logger.info(f"网格总数: {len(grid_data)}")
    logger.info(f"有建筑的网格: {(grid_data['coverage_ratio'] > 0).sum()}")
    logger.info(f"覆盖率范围: {grid_data['coverage_ratio'].min():.4f} ~ {grid_data['coverage_ratio'].max():.4f}")
    logger.info(f"温度范围: {grid_data['simulated_temp'].min():.2f}°C ~ {grid_data['simulated_temp'].max():.2f}°C")
    logger.info(f"平均温度: {grid_data['simulated_temp'].mean():.2f}°C")
    logger.info("="*60)


def main():
    """主函数"""
    try:
        config = Config()
        config.ensure_dirs()
        
        logger.info("="*60)
        logger.info("香港建筑密度与网格温度情景模拟")
        logger.info("="*60)
        
        # 1. 读取建筑数据
        buildings = read_building_data(config.BUILDING_DIR)
        
        # 2. 创建边界
        boundary = create_study_boundary(buildings)
        
        # 3. 创建网格
        grid = create_grid(boundary, config.CELL_SIZE)
        
        # 4. 计算建筑覆盖率
        grid_data = calculate_building_density(buildings, grid)
        
        # 5. 温度模拟
        grid_data = simulate_temperature(grid_data)
        
        # 6. 生成图表
        plot_results(grid_data, config.FIGURE_DIR)
        
        # 7. 统计
        print_statistics(grid_data)
        
        logger.info("\n✅ 分析完成！")
        logger.info(f"   图表: {config.FIGURE_DIR}")
        
    except Exception as e:
        logger.error(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
