# python-urban-data-portfolio
## Project Overview
This portfolio consists of three Python projects. The core project is an Accessibility Assessment of the 15-Minute Living Circle in Sha Tin District, Hong Kong, which utilizes GIS libraries such as GeoPandas and Shapely to conduct spatial coverage analysis of public transport, parks, and medical facilities, accurately identifying service gaps and outputting multi-dimensional visualizations and data files. Additionally, it includes two foundational applications—a Real Estate Commission Calculator and a Credit Card Debt Payment Forecaster—to demonstrate basic Python logic in conditional statements, iterative loops, and financial calculations. The entire portfolio is built using tools such as Python, Pandas, NumPy, Matplotlib, and GeoPandas.
## GIS-Based Accessibility Evaluation of Public Service Facilities within the 15-Minute Living Circle in Hong Kong
### Project Description
This project utilizes Python and GIS technologies such as GeoPandas to conduct a 15-minute living circle accessibility assessment in Sha Tin District, Hong Kong. Using a 500-meter grid as the basic analytical unit, the study applies 1250-meter walking buffer analysis to precisely calculate the coverage of bus stops, parks, and medical facilities within each grid cell, while identifying underserved areas. The results are presented through 2x3 multi-dimensional visualizations and exported as GeoJSON/CSV data files, offering an intuitive overview of facility distribution and service gaps to provide a data-driven foundation for optimizing community public resources.
### Program Output
<img width="1515" height="970" alt="Screenshot 2026-08-02 135238" src="https://github.com/user-attachments/assets/df29e302-c20e-4ab3-83bb-9ba613c8cb75" />

## Foundational Python projects
### 1)Commission Calculator
This is an interactive command-line program. Users select a property category and enter the selling price. The program looks up the corresponding commission rate via a dictionary mapping, performs a multiplication operation, and outputs the final agent commission.
#### Input: Property category, Selling price
#### Process: Dictionary lookup for commission rate → Selling price × Commission rate
#### Output: Agent commission amount
#### Program Output
<img width="1148" height="694" alt="image" src="https://github.com/user-attachments/assets/6567c5c3-cc83-4d63-9712-64f86b699eaf" />

### 2)Debt Payment Forecast
This is a predictive interactive program. Users input the remaining credit card balance, monthly payment amount, and interest rate. The program simulates the repayment process month by month using a While loop (deducting the monthly payment and calculating accrued interest) until the balance reaches zero, and finally outputs the total number of months required to clear the debt.
·Input: Credit card balance, Monthly payment, Interest rate
·Process: Loop simulation → Monthly deduction and interest calculation → Check if balance reaches zero
·Output: Total number of months to pay off the debt
#### Program Output
<img width="719" height="398" alt="image" src="https://github.com/user-attachments/assets/af424434-8d87-4fd9-99c9-0c0a2cd1568a" />

## Tools used
Python、Pandas、GeoPandas、Shapely、Matplotlib、NumPy





