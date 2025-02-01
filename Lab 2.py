def calculate_tax(price):
    tax_rate = 10.44 / 100
    return price * tax_rate

item = []
prices = []
max_total = 100
balance = max_total

while balance > 0:
    item_name = input('Enter item name (input "cancel" to quit): ')
    if item_name.lower() == "cancel":
        break
    if not item_name:
        print("Name cannot be empty.")
        continue

    try:
        price = float(input('Enter price: '))
        if price <= 0:
            print("Price must be greater than 0. Re-enter item name and price")
            continue

        total_price = price + calculate_tax(price)

        if balance - total_price >= 0:
            item.append(item_name)
            prices.append(price)
            balance -= total_price
            print(f" Your remaining balance is ", round(balance, 2))
        else:
            print("You have exceeded your budget. Your remaining balance is $", round(balance, 2))
            wants = input("Would you like to continue shopping within your budget? (yes/no): ")
            if wants.lower() != "yes":
                break

    except ValueError:
        print("Invalid input. Re-enter item name and price.")

