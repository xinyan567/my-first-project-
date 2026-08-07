#program name: stock management system
#Program Description: <Build a class called Stocks that manages the purchase and selling of stocks by customers in a
#financial company. The class consists of three attributes – customer number, customer name,
#and the stock balance for the customer.>


class Stocks:
def __init__(self, customer_code, customer_name, stock_balance):
self.customer_code = customer_code
self.customer_name = customer_name
self.stock_balance = stock_balance

def purchase(self, amount):
if amount <= 0:
            print("Error: Stock amount cannot be negative. Enter a positive value.")
return False
self.stock_balance += amount
return True

    def transfer(self, amount):
if amount <= 0:
            print("Error: Stock amount cannot be negative. Enter a positive value.")
return False
        if amount >self.stock_balance:
            print("Error: Insufficient stock to transfer.")
return False
self.stock_balance -= amount
return True

    def sell(self, amount):
if amount <= 0:
            print("Error: Stock amount cannot be negative. Enter a positive value.")
return False
        if amount >self.stock_balance:
            print("Error: Insufficient stock to sell.")
return False
self.stock_balance -= amount
return True

    def get_balance(self):
return self.stock_balance


def simulate_sample_output_1():
    print("\nSample Output 1:")
customer = Stocks("11348", "Toni Smith", 900)
    print(f"Customer code: {customer.customer_code}")
    print(f"Customer Name: {customer.customer_name}")
    print(f"Current Stock Balance: {customer.get_balance()}")

customer.purchase(100)
    print("Purchased Stock Amount: 100")

customer.transfer(200)
    print("Transferred Stock Amount: 200")

customer.sell(500)
    print("Stocks Sold: 500")

    print(f"Balance Stock Amount: {customer.get_balance()}")


def simulate_sample_output_2():
    print("\nSample Output 2:")
customer = Stocks("12948", "Al Greene", 1900)
    print(f"Customer code: {customer.customer_code}")
    print(f"Customer Name: {customer.customer_name}")
    print(f"Current Stock Balance: {customer.get_balance()}")

customer.purchase(100)
    print("Purchased Stock Amount: 100")

if not customer.transfer(-200):
        print("Transferred Stock Amount: -200")
        print("Error: Stock amount cannot be negative. Enter a positive value.")

customer.transfer(200)
    print("Transferred Stock Amount: 200")

customer.sell(500)
    print("Stocks Sold: 500")

    print(f"Balance Stock Amount: {customer.get_balance()}")


# Run the demos
simulate_sample_output_1()
simulate_sample_output_2()


def simulate_sample_output_3():
    print("\nSample Output 3:")
customer = Stocks("13777", "Lily Chen", 1200)
    print(f"Customer code: {customer.customer_code}")
    print(f"Customer Name: {customer.customer_name}")
    print(f"Current Stock Balance: {customer.get_balance()}")

# Attempt invalid purchase
if not customer.purchase(-150):
        print("Purchased Stock Amount: -150")
        print("Error: Stock amount cannot be negative. Enter a positive value.")

# Valid purchase
customer.purchase(300)
    print("Purchased Stock Amount: 300")

# Transfer
customer.transfer(400)
    print("Transferred Stock Amount: 400")

# Attempt to sell more than available
if not customer.sell(2000):
        print("Stocks Sold: 2000")
        print("Error: Insufficient stock to sell.")

# Valid sell
customer.sell(500)
    print("Stocks Sold: 500")

    print(f"Balance Stock Amount: {customer.get_balance()}")
simulate_sample_output_3()
