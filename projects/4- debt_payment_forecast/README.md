## Credit Card Debt Payment Period Predictor
## Project Description
This program predicts the number of payment periods required to pay off a credit card debt. Users input credit card information, current outstanding balance, monthly payment amount, and annual interest rate. The program simulates the monthly payment process to determine how many months it will take to fully repay the debt.
## Core Algorithm
The program uses a while loop to simulate the monthly payment process:
Calculate new balance each month:    
-New Balance = Current Balance × (1 + Monthly Interest Rate) - Monthly Payment  
-Monthly Interest Rate = Annual Interest Rate / 12 (Note: This program uses the annual rate directly without dividing by 12)  
If the new balance is less than 0, set it to 0 (preventing negative values)  
Increment counter by 1   
Continue loop while balance is greater than 0  
Return total number of payment periods  
## outputs
<img width="869" height="238" alt="image" src="https://github.com/user-attachments/assets/89f201aa-b0ce-4a11-b659-56124cb18ada" />
<img width="1424" height="381" alt="Screenshot 2026-08-06 012918" src="https://github.com/user-attachments/assets/0310b0a9-1219-496a-b672-83ed2ff38314" />

## Practical Applications  
Personal Financial Management: Help individuals plan credit card repayment strategies  
Financial Consulting Services: Provide clients with repayment time estimates  
Financial Education: Demonstrate the impact of compound interest on debt  
Banking Systems: Serve as an auxiliary tool for credit risk assessment  
