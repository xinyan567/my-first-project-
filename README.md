# python-urban-data-portfolio
# GIS-Based Accessibility Evaluation of Public Service Facilities within the 15-Minute Living Circle in Hong Kong
## Project Description
This project aims to evaluate the spatial accessibility and distributional equity of public service facilities within the "15-minute living circle" framework across Hong Kong. By integrating geospatial boundary data, demographic statistics, and Point-of-Interest (POI) data, the study quantifies the availability of essential community services—including public transit, parks, and healthcare facilities—within a 1,250-meter walking radius for each administrative district. The ultimate objective is to identify underserved regions and provide data-driven recommendations for urban planning and resource allocation.
## Research Data Object
Administrative Boundaries, Demographic Data, Bus Stops, Parks, Hospitals
## Data Structure
The spatial data is merged with demographic data using regional name fields as the join key. The final dataset contains region names, population counts, facility counts by category, total facilities, and the facilities-per-1,000-residents metric.
## Model Used
Four models are applied: coordinate transformation to the local projected system; spatial buffer analysis to create 1,250-meter walking zones; spatial intersection to count facilities within each zone; and a supply-demand evaluation model to calculate per-capita facility coverage and identify underserved districts.
## System flow
The workflow involves six steps: loading all datasets, unifying coordinate systems, merging population data with boundaries, generating buffers and performing intersection analysis, calculating evaluation metrics, and finally exporting results and visualizations.
## Program Output
### Conclusion:
The distribution of public service facilities within Hong Kong's 15-minute living circle is highly uneven. Core urban districts are heavily facility-rich but overly dominated by bus stops, with limited healthcare and park resources. In contrast, peripheral areas, especially the outlying islands and parts of the New Territories, suffer from severe service gaps, with some zones entirely lacking essential facilities such as hospitals.
### Recommendations:
To address these disparities, three actions are recommended: First, prioritize adding community clinics and transit links in facility-blind areas like the outlying islands. Second, restructure core urban zones by curbing excessive bus stops and reallocating space for more parks and medical facilities. Third, establish a dynamic monitoring system using the "facilities per 1,000 residents" metric to ensure infrastructure growth aligns with population changes in new development areas.
<img width="1079" height="868" alt="Screenshot 2026-08-01 142152" src="https://github.com/user-attachments/assets/1a1e595b-8319-477c-b976-3cadd0e0e0af" />
<img width="675" height="501" alt="Screenshot 2026-08-01 142009" src="https://github.com/user-attachments/assets/e65c9e79-b4c0-496f-8c93-1f623a882bbf" />
<img width="682" height="513" alt="Screenshot 2026-08-01 142035" src="https://github.com/user-attachments/assets/9cbf2c09-96b2-4d8e-8a0c-c65b3916d363" />
<img width="1527" height="700" alt="Screenshot 2026-08-01 142120" src="https://github.com/user-attachments/assets/34d40bb4-dfeb-40a6-90fe-31aac3f7be17" />
# Commission Calculator
## Project Description
This project is a Real Estate Agent Commission Calculator. It allows users to select a property category and enter the property's selling price. The system calculates and displays the commission earned by the real estate agent based on the commission rate assigned to each property category.
## Research Data Object
Property Category,Property Selling Price,Commission Rate,Agent Commission
## Data Structure
Dictionary,User Input,Selection Structure
## Model Used
Rule-Based Decision Model,Dictionary Lookup Model
## System flow
User Input
      |
Dictionary Lookup
      |
Commission Rate
      |
Multiplication Formula
      |
Output Result
## Program Output
<img width="1149" height="783" alt="Screenshot 2026-07-31 111239" src="https://github.com/user-attachments/assets/1f382d96-9b0d-4d79-9f57-dbb4724b401a" />
<img width="1148" height="694" alt="image" src="https://github.com/user-attachments/assets/6567c5c3-cc83-4d63-9712-64f86b699eaf" />
<img width="1139" height="679" alt="Screenshot 2026-07-31 111352" src="https://github.com/user-attachments/assets/ba92a478-a13f-485b-9aba-8c74b19fe8c5" />



# Debt Payment Forecast
## Project Description
This project is a Credit Card Debt Payment Forecast System. Users enter their credit card information, remaining balance, monthly payment amount, and interest rate. The system estimates the number of monthly payments required to completely repay the credit card debt.
## Research Data Object
Credit Card Number,Cardholder Name,Remaining Balance,Monthly Payment,Interest Rate,Number of Payments
## Data Structure
Variables,Function,While Loop,Arithmetic Calculation
## Model Used
Iterative Simulation Model
## System flow
User Input
      |
Read Credit Card Information
      |
Input Remaining Balance
      |
Input Monthly Payment
      |
Input Interest Rate
      |
While Loop Simulation
      |
Calculate Remaining Balance
      |
Debt Paid Off?
      |
Yes ---> Display Number of Payments
## Program Output
<img width="719" height="398" alt="image" src="https://github.com/user-attachments/assets/af424434-8d87-4fd9-99c9-0c0a2cd1568a" />

# Customer Stock Account Management System
## Project Description
This project develops a Stock Management System using Object-Oriented Programming (OOP) in Python. The system manages customer stock accounts by allowing customers to purchase, transfer, and sell stocks while validating transactions and maintaining the current stock balance.
## Research Data Object
Customer Code, Customer Name, Stock Balance, Purchase Amount, Transfer Amount, Selling Amount
## Data Structure
Class, Object, Attributes, Methods
## Model Used
Object-Oriented Programming (OOP) Model
## System flow
Create Customer Account
        |
Input Customer Information
        |
Choose Transaction
        |
Purchase / Transfer / Sell
        |
Validate Input
        |
Update Stock Balance
        |
Display Current Balance
## Program Output
<img width="657" height="704" alt="image" src="https://github.com/user-attachments/assets/601845af-3f4e-4c16-b2c1-9f35b1234692" />



