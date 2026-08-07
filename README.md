# Python and Urban Data Analysis Portfolio

This repository presents selected Python projects in spatial analysis,
urban accessibility and data processing.

## Featured Project
### 1) Hong Kong Facility Accessibility Analysis
Tools: Python, GeoPandas, Pandas, Shapely and Matplotlib.  
The project analyses the spatial relationship between residential areas
and public transport, parks and healthcare facilities.

This project utilizes Python and GIS technologies such as GeoPandas to conduct a 15-minute living circle accessibility assessment in Sha Tin District, Hong Kong. Using a 500-meter grid as the basic analytical unit, the study applies 1250-meter walking buffer analysis to precisely calculate the coverage of bus stops, parks, and medical facilities within each grid cell, while identifying underserved areas. The results are presented through 2x3 multi-dimensional visualizations and exported as GeoJSON/CSV data files, offering an intuitive overview of facility distribution and service gaps to provide a data-driven foundation for optimizing community public resources.
### Program Outputs
<img width="1515" height="970" alt="Screenshot 2026-08-02 135238" src="https://github.com/user-attachments/assets/df29e302-c20e-4ab3-83bb-9ba613c8cb75" />

### 2) Hong Kong Urban Heat Scenario Simulation
Tools: Python, GeoPandas, Pandas, Fiona, Shapely, NumPy, Matplotlib.  
This project calculates building coverage ratios across 1km grids in Hong Kong and simulates surface temperature distributions using a urban heat island coefficient. The positive correlation between building density and temperature is visualized through scatter plots, boxplots, and spatial distribution maps.
### Program Outputs
<img width="1704" height="1018" alt="image" src="https://github.com/user-attachments/assets/2b81261f-0f19-4e0f-8e00-5f61cb24406e" />
<img width="1676" height="1222" alt="image" src="https://github.com/user-attachments/assets/ec3d45e8-a8e4-4633-9d24-e5b87d17a03f" />
<img width="1670" height="1126" alt="image" src="https://github.com/user-attachments/assets/5e5a5f84-77d1-4b0e-b8f1-42dabbb28d12" />



## Foundational Python projects
### 1)Commission Calculator
This is an interactive command-line program. Users select a property category and enter the selling price. The program looks up the corresponding commission rate via a dictionary mapping, performs a multiplication operation, and outputs the final agent commission.  
(Input: Property category, Selling price
|Process: Dictionary lookup for commission rate → Selling price × Commission rate
|Output: Agent commission amount)
#### Program Output
<img width="1148" height="694" alt="image" src="https://github.com/user-attachments/assets/6567c5c3-cc83-4d63-9712-64f86b699eaf" />

### 2)Debt Payment Forecast
This is a predictive interactive program. Users input the remaining credit card balance, monthly payment amount, and interest rate. The program simulates the repayment process month by month using a While loop (deducting the monthly payment and calculating accrued interest) until the balance reaches zero, and finally outputs the total number of months required to clear the debt.  
(Input: Credit card balance, Monthly payment, Interest rate
|Process: Loop simulation → Monthly deduction and interest calculation → Check if balance reaches zero
|Output: Total number of months to pay off the debt)
#### Program Output
<img width="719" height="398" alt="image" src="https://github.com/user-attachments/assets/af424434-8d87-4fd9-99c9-0c0a2cd1568a" />

### 3)Stock Management System
Stock Management System is an interactive command-line stock transaction management system. Users create customer accounts and perform stock purchase, transfer, and sale operations. The program is designed using Object-Oriented Programming (OOP) principles, encapsulating customer information and transaction logic within the Stocks class. All transaction operations include input validation and error handling mechanisms to ensure stock balance accuracy and data integrity.   
(Input: Customer code, Customer name, Initial stock balance, Transaction amount | Process: Class instantiation → Method invocation → Amount validation → Balance update | Output: Transaction status feedback, Updated stock balance)
#### Program Output
<img width="844" height="216" alt="image" src="https://github.com/user-attachments/assets/aa28e0b0-5eb5-498d-9a6f-bd0f21d81950" />

## Tools used
Python, Pandas, GeoPandas, Shapely, Matplotlib, NumPy, Fiona.





