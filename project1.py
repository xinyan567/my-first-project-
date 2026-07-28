#/*-------------------------------------------------------------------------------
# Name:         Xinyan Li
# Student ID:   007573720001
# Email:        xli29@una.edu
# Course Information: <CIS 225 01>
# Program Source File Name: <real_estate_agents.py>
# Programming Assignment: #1
# Program Description:< A program which allow users to input for the category and 
#                   the sales amount of the property being sold,and users will receive 
#                   the output of the amount an agent receives after the sale. >
# References:
# Due Date: Mar 10 by 11.59pm
#   In keeping with the honor code policies of the University of University of North Alabama, the
# School of Business, and the Department of Computer Science, I affirm that I have neither
# given nor received on this programming assignment. This assignment
# represents my individual, original effort.
# Xinyan Li ---My Signature is on File
#*/-------------------------------------------------------------------------------

#print the table
print("---------------------------------------------------------------------")
print("|           Category            |      Agent:Percentage of Sales    |")
print("---------------------------------------------------------------------")
print("| 1.Residential Real Estate     |                 5%                |")
print("---------------------------------------------------------------------")
print("| 2.Commercial Real Estate      |                 6%                |")
print("---------------------------------------------------------------------")
print("| 3.Industrial Real Estate      |                6.2%               |")
print("---------------------------------------------------------------------")
print("| 4.Agricultural Real Estate    |                5.8%               |")
print("---------------------------------------------------------------------")
print("| 5.Special Purpose Real Estate |                6.5%               |")
print("---------------------------------------------------------------------")
print("| 6.Mixed-Use Real Estate       |                5.8%               |")
print("---------------------------------------------------------------------")

#Define a dictionary including the data of Category and Percetage of sales
category={"1":0.05, "2":0.06 , "3":0.062, "4":0.058 , "5":0.065 , "6":0.058}

#let users input the choice of category and the price of the ssale item
Category_choose=(input('Enter the Category based off the table above: '))

#use if-else statement to judge if the scope of category is valid or not,and print the result out
if Category_choose not in category:
    print("Invalid Category!")
else:
    price=float(input('Enter the price of the sale item: $ '))
    Agent_percent_sales=price*category[Category_choose]

#print the result and keep 2 decimal places
    print(f'Agent percentage of sales       : $ {Agent_percent_sales:.2f}')
