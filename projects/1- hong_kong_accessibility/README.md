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

## Analysis Overview
Region name: Sha Tin District
Number of analysis grid points: 274
Grid precision: 500 meters
## 15-Minute Life Circle Compliance
Number of compliant grid points: 35 (12.8%)
Number of non-compliant grid points: 239 (87.2%)
## Facility Coverage
Average number of facilities per point: 20.95
Average number of bus stops: 20.02
Average number of parks: 0.63
Average number of hospitals: 0.30
## Underserved Areas
Number of underserved grid points: 65
Proportion of underserved areas: 23.7%
Areas with no facilities at all: 59

## Results Summary
### Key Findings
The 15-minute living circle analysis of Sha Tin District reveals:
| Indicator | Result |
|-----------|--------|
| Compliance Rate | 12.8% (35/274 grid points) |
| Average Facilities per Point | 20.95 |
| Underserved Areas | 65 grid points (23.7%) |
| Areas with No Facilities | 59 grid points (21.5%) |

### Key Conclusions
1. **Good public transport coverage**: The bus stop network is well-developed, with 59.9% of areas reaching the "very rich" facility level.
2. **Severe shortage of parks and medical facilities**: On average, each grid point has only 0.63 parks and 0.30 hospitals, far below the living circle standard.
3. **Significant facility blind spots**: 21.5% of the area has no facilities at all, mainly concentrated in the southern and eastern fringe areas of Sha Tin District.

### Planning Implications
- Prioritize the development of community comprehensive facilities in the **59 facility-blind grid points**
- **Increase green space** in areas with low park coverage
- **Add primary medical facilities** in underserved areas
- Future planning should focus on **balanced allocation of facility types**, rather than simply increasing the quantity of a single facility type

This study provides data support and decision-making reference for urban facility planning in Sha Tin District.

