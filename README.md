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
This project is a Real Estate Agent Commission Calculator. It allows users to select a property category and enter the property's selling price. The system calculates and displays the commission earned by the real estate agent based on the commission rate assigned to each property category.
### Research Data Object
Property Category,Property Selling Price,Commission Rate,Agent Commission
### System flow
User Input
      |
Dictionary Lookup
      |
Commission Rate
      |
Multiplication Formula
      |
Output Result
### Program Output
<img width="1149" height="783" alt="Screenshot 2026-07-31 111239" src="https://github.com/user-attachments/assets/1f382d96-9b0d-4d79-9f57-dbb4724b401a" />
<img width="1148" height="694" alt="image" src="https://github.com/user-attachments/assets/6567c5c3-cc83-4d63-9712-64f86b699eaf" />
<img width="1139" height="679" alt="Screenshot 2026-07-31 111352" src="https://github.com/user-attachments/assets/ba92a478-a13f-485b-9aba-8c74b19fe8c5" />



### 2)Debt Payment Forecast
### Project Description
This project is a Credit Card Debt Payment Forecast System. Users enter their credit card information, remaining balance, monthly payment amount, and interest rate. The system estimates the number of monthly payments required to completely repay the credit card debt.
### Research Data Object
Credit Card Number,Cardholder Name,Remaining Balance,Monthly Payment,Interest Rate,Number of Payments
### System flow
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
### Program Output
<img width="719" height="398" alt="image" src="https://github.com/user-attachments/assets/af424434-8d87-4fd9-99c9-0c0a2cd1568a" />

## Tools used
Python、Pandas、GeoPandas、Shapely、Matplotlib、NumPy





