def calculate_tax(price):
    tax_rate = 10.44 / 100
    return price * tax_rate
item = []
prices =[]
max_total = 100
balance = 100 - sum(prices)
price_count = 0
while sum(prices) < max_total:
    item_name = input('Enter item name(input "cancel" to quit): ')
    if item_name.lower() == "cancel":
        break
    if not item_name:
        print("Name cannot be empty.")
        continue
    try:
        price = float(input('Enter price: '))
        price_count += calculate_tax(price)
        if price_count > max_total:
            
            item.append(item_name)
            prices.append(price)
        else:
            print("Price must be greater than 0. Re-enter item name and price")
    except ValueError:
        print(" Invalid input. Re-enter item name and price")