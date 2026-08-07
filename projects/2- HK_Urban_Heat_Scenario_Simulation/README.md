## Hong Kong Building Density and Grid-Based Temperature Scenario Simulation
## Project Overview
This project simulates the relationship between building density and urban heat island (UHI) effects in Hong Kong using a grid-based analytical approach. It processes building footprint data, calculates building coverage ratios across a regular grid, and performs scenario simulations to model temperature variations based on building density.

## Features
- Building Data Processing: Reads and processes building footprint data from Shapefile (SHP) format  
- Grid Generation: Creates a systematic grid (default 1000m × 1000m cells) covering the study area  
- Building Coverage Calculation: Computes building coverage ratios for each grid cell  
- Temperature Simulation: Simulates temperature patterns based on building density with configurable UHI coefficients  
- Visualization: Generates three key analytical figures:  
  Scatter plot showing the relationship between coverage ratio and temperature  
  Box plot comparing high-density vs. low-density areas  
  Spatial distribution map of simulated temperatures  


## outputs
<img width="1760" height="1116" alt="Screenshot 2026-08-06 012323" src="https://github.com/user-attachments/assets/4f3d4997-dbdc-49c8-89b3-7950de7ec091" />
<img width="1722" height="1228" alt="Screenshot 2026-08-06 012540" src="https://github.com/user-attachments/assets/d975e52d-18ac-4850-85aa-6e0727a1d363" />
<img width="1768" height="1171" alt="Screenshot 2026-08-06 012559" src="https://github.com/user-attachments/assets/b761977d-7737-4446-964c-48152b25b299" />

## Results Summary
This scenario simulation reveals a positive correlation between building density and simulated temperature across Hong Kong. The analysis demonstrates that areas with higher building coverage ratios tend to exhibit elevated temperatures, consistent with urban heat island theory.

## Key Findings
Building coverage ratios range from 0 to 0.0225 (2.25%) across the study area, with 429 grid cells containing buildings. The simulation indicates that high-density areas show higher temperatures compared to low-density areas, with a mean temperature difference of approximately 1.5°C under the current scenario settings.

## Visualization Outputs
Three analytical figures were generated:  
Figure 1 – Scatter plot showing a positive trend between building coverage ratio and simulated temperature (R² ≈ 0.86), indicating that increased building density is associated with higher temperatures.  
Figure 2 – Box plot comparing temperature distributions between high-density and low-density grid cells, demonstrating a clear thermal distinction between the two groups.  
Figure 3 – Spatial distribution map of simulated temperatures across the 1km × 1km grid, highlighting areas with elevated temperatures concentrated in regions with higher building densities.  

## Important Note
This is a scenario simulation based on the assumption: Temperature = Base Temperature + (Coverage Ratio × UHI Coefficient) + Noise. The results represent modeled patterns rather than actual measured temperatures. For real-world urban heat island analysis, observed temperature data from meteorological stations and additional environmental variables (e.g., vegetation, land use) would be required.


