## Project: 15-Minute Living Circle Analysis - Sha Tin District, Hong Kong
This project analyzes the accessibility of public transport (bus stops), 
parks, and medical facilities within a 15-minute walking distance (1,250 meters) 
for residents in Sha Tin District, Hong Kong.

The analysis uses grid-based sampling to evaluate:
1. Facility coverage distribution across the district
2. Identification of underserved areas (facilities < 2)
3. Assessment of 15-minute living circle standards (public transport + park + hospital)

Data Sources:
- Boundary data: ./data/boundary.geojson
- Population data: ./data/boundary.CSV  
- Bus stops: ./data/bus.geojson
- Parks: ./data/parks.geojson
- Hospitals: ./data/hospitals.geojson

Basic Statistics: Total analysis grid points: 274
Points meeting the 15-minute life circle standard: 35 (12.8%)
Average number of facilities per point: 20.95
Average number of bus stops: 20.02
Average number of parks: 0.63
Average number of hospitals: 0.30

Facility level distribution:
Very rich in facilities: 164 points (59.9%)
No facilities: 59 points (21.5%)
Rich in facilities: 25 points (9.1%)
Basically adequate: 14 points (5.1%)
Insufficient facilities: 12 points (4.4%)

  <img width="1620" height="1044" alt="Screenshot 2026-08-05 165459" src="https://github.com/user-attachments/assets/69696bf9-0ff2-42bd-94a7-6449af6e2589" />

Analysis Overview
==================================================
Region name: Sha Tin District
Number of analysis grid points: 274
Grid precision: 500 meters

15-Minute Life Circle Compliance
==================================================
Number of compliant grid points: 35 (12.8%)
Number of non-compliant grid points: 239 (87.2%)

Facility Coverage
==================================================
Average number of facilities per point: 20.95
Average number of bus stops: 20.02
Average number of parks: 0.63
Average number of hospitals: 0.30

Underserved Areas
==================================================
Number of underserved grid points: 65
Proportion of underserved areas: 23.7%
Areas with no facilities at all: 59

## Results Summary
### 主要发现

沙田区15分钟生活圈分析显示：

| 指标 | 结果 |
|------|------|
| 达标率 | 12.8%（35/274个网格点） |
| 平均设施数 | 20.95个/网格点 |
| 服务不足区域 | 65个网格点（23.7%） |
| 完全无设施区域 | 59个网格点（21.5%） |

### 关键结论

1. **公共交通覆盖良好**：巴士站网络密集，59.9%的区域设施丰富度达到"非常丰富"级别

2. **公园和医疗设施严重不足**：平均每个网格点仅有0.63个公园和0.30个医院，远低于生活圈标准

3. **存在明显设施盲区**：21.5%的区域完全没有设施，主要集中在沙田区南部和东部边缘地带

### 规划启示

- 优先在**59个无设施网格点**建设社区综合设施
- 在公园覆盖率低的区域**增加绿地空间**
- 在服务不足区域**增设基层医疗设施**
- 未来规划应注重**设施类型的均衡配置**，而非仅增加单一类型设施

本研究为沙田区的城市设施规划提供了数据支撑和决策参考。

