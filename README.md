# python-urban-data-portfolio

# GIS-Based Accessibility Evaluation of Public Service Facilities within the 15-Minute Living Circle in Hong Kong
## Project Description
This project aims to evaluate the spatial accessibility and distributional equity of public service facilities within the "15-minute living circle" framework across Hong Kong. By integrating geospatial boundary data, demographic statistics, and Point-of-Interest (POI) data, the study quantifies the availability of essential community services—including public transit, parks, and healthcare facilities—within a 1,250-meter walking radius for each administrative district. The ultimate objective is to identify underserved regions and provide data-driven recommendations for urban planning and resource allocation.
## Research Data Object
Administrative Boundaries, Demographic Data, Bus Stops, Parks, Hospitals
## Data Structure
The spatial data is merged with demographic data using regional name fields as the join key. The final dataset contains region names, population counts, facility counts by category, total facilities, and the facilities-per-1,000-residents metric.
## System flow
The workflow involves six steps: loading all datasets, unifying coordinate systems, merging population data with boundaries, generating buffers and performing intersection analysis, calculating evaluation metrics, and finally exporting results and visualizations.
## Program Output
<img width="1515" height="970" alt="Screenshot 2026-08-02 135238" src="https://github.com/user-attachments/assets/df29e302-c20e-4ab3-83bb-9ba613c8cb75" />

# Commission Calculator
## Project Description
This project is a Real Estate Agent Commission Calculator. It allows users to select a property category and enter the property's selling price. The system calculates and displays the commission earned by the real estate agent based on the commission rate assigned to each property category.
## Research Data Object
Property Category,Property Selling Price,Commission Rate,Agent Commission
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





