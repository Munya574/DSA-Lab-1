import os
import datetime
import csv
# Constants
TAX_RATE = 0.1044
STORE_NAME = "GROUP 5 STORE"

category_data = {
        "f": ("FOOD", [], []),
        "c": ("CLOTHING", [], []),
        "e": ("ELECTRONICS", [], []),
        "p": ("PHARMACEUTICALS", [], [])
    }

CATALOG = {
    "f": {
        "name": "FOOD",
        "items": {
            "Apple": 1.00,
            "Banana": 0.50,
            "Bread": 2.50,
            "Milk": 3.00,
            "Eggs": 2.00
        }
    },
    "c": {
        "name": "CLOTHING",
        "items": {
            "T-Shirt": 15.00,
            "Jeans": 40.00,
            "Jacket": 60.00,
            "Socks": 5.00,
            "Hat": 10.00
        }
    },
    "e": {
        "name": "ELECTRONICS",
        "items": {
            "Headphones": 50.00,
            "Smartphone": 500.00,
            "Laptop": 1000.00,
            "Tablet": 300.00,
            "Charger": 20.00
        }
    },
    "p": {
        "name": "PHARMACEUTICALS",
        "items": {
            "Aspirin": 5.00,
            "Band-Aids": 3.00,
            "Vitamins": 10.00,
            "Cold Medicine": 7.00,
            "Antibiotics": 15.00
        }
    }
}
# Categories configuration
#CATEGORIES = {
   # "f": ("FOOD", "food"),
    #"c": ("CLOTHING", "clothing"),
    #"e": ("ELECTRONICS", "electronics"),
    #"p": ("PHARMACEUTICALS", "pharmaceuticals")
#}

def calculate_tax(price):
    return price * TAX_RATE

def get_totals(prices):
    total_before_tax = sum(prices)
    total_tax = sum(calculate_tax(price) for price in prices)
    return total_before_tax, total_tax, total_before_tax + total_tax

def generate_transaction_id():
    existing_ids = get_existing_transaction_ids()
    while True:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        transaction_id = f"ND-{timestamp}"
        if transaction_id not in existing_ids:
            return transaction_id

def get_existing_transaction_ids():
    receipts_dir = "receipts"
    if not os.path.exists(receipts_dir):
        return set()
    return {filename.split('_')[0] for filename in os.listdir(receipts_dir) 
            if filename.endswith('_receipt.txt')}

def create_receipt_text(transaction_id, items, prices):
    total_before_tax, total_tax, total_after_tax = get_totals(prices)
    
    receipt = []
    receipt.append("=" * 40)
    receipt.append(f"{{:^40}}".format(STORE_NAME))
    receipt.append("{:^40}".format("Tax Receipt"))
    receipt.append("=" * 40)
    receipt.append(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    receipt.append(f"Transaction ID: {transaction_id}")
    receipt.append("-" * 40)
    
    # Display categorized items
    for item, price in zip(items, prices):
        receipt.append(f"{item:<25} ${price:>9.2f}")
   # for category_key, (category_name, items_list, prices_list) in category_data.items():
    #    if items_list:
     #       receipt.append(f"\n{category_name}:")
      #      for item, price in zip(items_list, prices_list):
       #         receipt.append(f"{item:<25} ${price:>9.2f}")
    
    # Totals
    receipt.append("\n" + "-" * 40)
    receipt.append(f"{'Subtotal:':<25} ${total_before_tax:>9.2f}")
    receipt.append(f"{'Tax (10.44%):':<25} ${total_tax:>9.2f}")
    receipt.append(f"{'TOTAL:':<25} ${total_after_tax:>9.2f}")
    receipt.append("=" * 40)
    receipt.append("\nThank you for your purchase!")
    receipt.append("Please keep this receipt for your records.")
    
    return "\n".join(receipt)

def save_receipt_to_csv(transaction_id, items, prices, category_data):
    receipts_file = "receipts.csv"
    file_exists = os.path.isfile(receipts_file)
    
    with open(receipts_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        
        # Write header if file doesn't exist
        if not file_exists:
            writer.writerow([
                "TransactionID", "Date", "Category", "Item", "Quantity", 
                "PricePerUnit", "TotalPrice", "Subtotal", "Tax", "Total"
            ])
        
        # Calculate totals
        subtotal = sum(prices)
        tax = subtotal * TAX_RATE
        total = subtotal + tax
        
        # Write each item in the transaction
        for item, price in zip(items, prices):
            item_name, quantity = item.split(" x")
            category = "FOOD"  # Replace with logic to get the correct category
            writer.writerow([
                transaction_id,
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                category,
                item_name,
                quantity,
                price / int(quantity),  # Price per unit
                price,  # Total price for the item
                subtotal,
                tax,
                total
            ])
    
    print(f"\nReceipt data has been saved to {receipts_file}")

def display_cart(items, prices):
    total_before_tax, total_tax, total_after_tax = get_totals(prices)
    print("\n" + "=" * 40)
    print("{:^40}".format("SHOPPING CART"))
    print("=" * 40)
    
    #item_index = 0
    #for category_key, (category_name, items, prices_list) in category_data.items():
     #   if items:
      #      print(f"\n{category_name}:")
    print("{:<5} {:<25} {:>12}".format("No.", "Item", "Price ($)"))
    print("-" * 40)
    for i, (item, price) in enumerate(zip(items, prices)):
                print(f"{i:<5} {item:<25} ${price:>9.2f}")
            #item_index += len(items)
    
    print("\n" + "-" * 40)
    print(f"{'Subtotal:':<25} ${total_before_tax:>9.2f}")
    print(f"{'Tax:':<25} ${total_tax:>9.2f}")
    print(f"{'Total:':<25} ${total_after_tax:>9.2f}")
    print("=" * 40)
    #return item_index  # Total number of items

def checkout_process(items, prices):
    while True:
        #total_items = 
        display_cart(items, prices)
        
        print("\nOptions:")
        print("1. Complete Checkout")
        print("2. Remove Item")
        print("3. Cancel Transaction")
        choice = input("\nEnter choice (1/2/3): ").strip()
        
        if choice == "1":
            if not items:
                print("\nCart is empty. Add items before checkout.")
                continue
            transaction_id = generate_transaction_id()
            receipt_text = create_receipt_text(transaction_id, items, prices)
            save_receipt_to_csv(transaction_id, items, prices, category_data)
            print("\nCheckout complete! Thank you for shopping!")
            return True
        
        elif choice == "2":
            if not items:
                print("\nNo items to remove.")
                continue
            try:
                remove_index = int(input(f"Enter item number (0-{len(items)-1}): "))
                if 0 <= remove_index < len(items):
                    # Find which category contains the item
                    #current_index = 0
                    #for category_key, (category_name, items_list, prices_list) in category_data.items():
                     #   if current_index <= remove_index < current_index + len(items_list):
                           # local_index = remove_index - current_index
                            removed_item = items.pop(remove_index)
                            removed_price = prices.pop(remove_index)
                           # items.remove(removed_item)
                            #prices.remove(removed_price)
                            print(f"\nRemoved {removed_item} (${removed_price:.2f})")
                            return
                        #current_index += len(items_list)
                else:
                    print("\nInvalid item number.")
            except ValueError:
                print("\nInvalid input. Please enter a number.")
        
        elif choice == "3":
            print("\nTransaction cancelled.")
            items.clear()
            prices.clear()
            #for _, (_, items_list, prices_list) in category_data.items():
             #   items_list.clear()
              #  prices_list.clear()
            return False
        
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")

def main():
    items = []
    prices = []
    category_data = {
        "f": ("FOOD", [], []),
        "c": ("CLOTHING", [], []),
        "e": ("ELECTRONICS", [], []),
        "p": ("PHARMACEUTICALS", [], [])
    }
    while True:
        print("\nSelect a category:")
        for key, value in CATALOG.items():
            print(f"{key}. {value['name']}")
        print("x. Checkout")
        print("q. Quit")
        choice = input("Enter your choice: ").strip().lower()
        
        if choice == "q":
            print("\nThank you for visiting! Goodbye!")
            break
        elif choice == "x":
            if not items:
                print("\nCart is empty. Please add items first.")
                continue
            if checkout_process(items, prices):
                break
        elif choice in CATALOG:
            category = CATALOG[choice]
            print(f"\n{category['name']} Items:")
            item_list = list(category['items'].items())
            for i, (item, price) in enumerate(item_list, start=1):
                print(f"{i}. {item}: ${price:.2f}")
            
            try:
                item_number = int(input("\nEnter the number of the item you want to add: "))
                if item_number < 1 or item_number > len(item_list):
                    print("Invalid item number. Please try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            
            item_name, item_price = item_list[item_number - 1]
            
            try:
                quantity = int(input(f"How many {item_name}(s) do you want? "))
                if quantity <= 0:
                    print("Quantity must be greater than 0.")
                    continue
            except ValueError:
                print("Invalid quantity. Please enter a number.")
                continue
            
            total_price = item_price * quantity
            items.append(f"{item_name} x{quantity}")
            prices.append(total_price)
            
            print(f"Added {item_name} x{quantity} (${total_price:.2f}) to your cart.")
            print(f"Running total (without tax): ${sum(prices):.2f}")
        else:
            print("Invalid choice. Please try again.")
            #print("\nEnter: 'q' to quit, 'c' to checkout")
        #item_name = input("Enter item name: ").strip()
        
      #  if item_name.lower() == "q":
       #     break
       # elif item_name.lower() == "c":
        #    if items:
         #       if checkout_process(items, prices, category_data):
          #          break
           # else:
            #    print("Cart is empty. Please add items first.")
            #continue
        
      #  if not item_name:
       #     print("Name cannot be empty.")
        #    continue
        
       # try:
        #    price = float(input("Enter price: "))
         #   if price <= 0:
          #      print("Price must be greater than 0.")
      #          continue
       # except ValueError:
        #    print("Invalid price. Please enter a number.")
         #   continue
        #
     #   category = input("Enter category (f = food, c = clothing, e = electronics, p = pharmaceuticals): ").strip().lower()
      #  if category not in CATEGORIES:
       #     print("Invalid category. Use 'f', 'c', 'e', or 'p'.")
        #    continue
        
       # category_name, items_list, prices_list = category_data[category]
        #items_list.append(item_name)
      #  prices_list.append(price)
       # items.append(item_name)
        #prices.append(price)
        
       # print(f"Added {item_name} (${price:.2f}) to {category_name}")
       # print(f"Running total (without tax): ${sum(prices):.2f}")

if __name__ == "__main__":
    main()