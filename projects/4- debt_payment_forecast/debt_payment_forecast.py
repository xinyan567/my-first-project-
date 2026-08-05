# Name: Li Xinyan
# Program Description: <Write a program in Python to forecast the number of payments required to pay off a credit card debt.>

print('HLinings Credit Card Debt: Forecasting the number of payments left to pay')
print('--------------------------------------------------------------------------------------------------')
card_number=int(input('Enter the credit card number: '))
cardholder=input('Enter the name of the cardholder: ')
balance_left_pay=float(input('Input the balance left to be paid on the card:$ '))
each_month_payoff=float(input('Input the payment that the cardholder will pay off each month: $ '))
interest_rate=float(input('Input the interest rate applied: '))
def count_payment(balance_left_pay):
    count=0
    while balance_left_pay>0:
        balance_left_pay=(balance_left_pay)*(1+interest_rate)-each_month_payoff
        if balance_left_pay<0:
            balance_left_pay=0
        count+=1
    return count
times=count_payment(balance_left_pay)
print(times,'payments')
