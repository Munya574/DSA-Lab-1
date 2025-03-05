import os
import datetime

# Constants
TAX_RATE = 0.1044
STORE_NAME = "GROUP 5 STORE"

# Categories configuration
CATEGORIES = {
    "f": ("FOOD", "food"),
    "c": ("CLOTHING", "clothing"),
    "e": ("ELECTRONICS", "electronics"),
    "p": ("PHARMACEUTICALS", "pharmaceuticals")
}

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

def create_receipt_text(transaction_id, items, prices, category_data):
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
    for category_key, (category_name, items_list, prices_list) in category_data.items():
        if items_list:
            receipt.append(f"\n{category_name}:")
            for item, price in zip(items_list, prices_list):
                receipt.append(f"{item:<25} ${price:>9.2f}")
    
    # Totals
    receipt.append("\n" + "-" * 40)
    receipt.append(f"{'Subtotal:':<25} ${total_before_tax:>9.2f}")
    receipt.append(f"{'Tax (10.44%):':<25} ${total_tax:>9.2f}")
    receipt.append(f"{'TOTAL:':<25} ${total_after_tax:>9.2f}")
    receipt.append("=" * 40)
    receipt.append("\nThank you for your purchase!")
    receipt.append("Please keep this receipt for your records.")
    
    return "\n".join(receipt)

def save_receipt_to_txt(receipt_text, transaction_id):
    os.makedirs("receipts", exist_ok=True)
    file_path = os.path.join("receipts", f"{transaction_id}_receipt.txt")
    try:
        with open(file_path, "w") as file:
            file.write(receipt_text)
        print(f"\nYour receipt has been saved to {file_path}")
    except IOError as e:
        print(f"\nError saving receipt: {e}")

def display_cart(category_data, prices):
    total_before_tax, total_tax, total_after_tax = get_totals(prices)
    print("\n" + "=" * 40)
    print("{:^40}".format("SHOPPING CART"))
    print("=" * 40)
    
    item_index = 0
    for category_key, (category_name, items, prices_list) in category_data.items():
        if items:
            print(f"\n{category_name}:")
            print("{:<5} {:<25} {:>12}".format("No.", "Item", "Price ($)"))
            print("-" * 40)
            for i, (item, price) in enumerate(zip(items, prices_list), item_index):
                print(f"{i:<5} {item:<25} ${price:>9.2f}")
            item_index += len(items)
    
    print("\n" + "-" * 40)
    print(f"{'Subtotal:':<25} ${total_before_tax:>9.2f}")
    print(f"{'Tax:':<25} ${total_tax:>9.2f}")
    print(f"{'Total:':<25} ${total_after_tax:>9.2f}")
    print("=" * 40)
    return item_index  # Total number of items

def checkout_process(items, prices, category_data):
    while True:
        total_items = display_cart(category_data, prices)
        
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
            receipt_text = create_receipt_text(transaction_id, items, prices, category_data)
            save_receipt_to_txt(receipt_text, transaction_id)
            print("\nCheckout complete! Thank you for shopping!")
            return True
        
        elif choice == "2":
            if not items:
                print("\nNo items to remove.")
                continue
            try:
                remove_index = int(input(f"Enter item number (0-{total_items-1}): "))
                if 0 <= remove_index < total_items:
                    # Find which category contains the item
                    current_index = 0
                    for category_key, (category_name, items_list, prices_list) in category_data.items():
                        if current_index <= remove_index < current_index + len(items_list):
                            local_index = remove_index - current_index
                            removed_item = items_list.pop(local_index)
                            removed_price = prices_list.pop(local_index)
                            items.remove(removed_item)
                            prices.remove(removed_price)
                            print(f"\nRemoved {removed_item} (${removed_price:.2f})")
                            break
                        current_index += len(items_list)
                else:
                    print("\nInvalid item number.")
            except ValueError:
                print("\nInvalid input. Please enter a number.")
        
        elif choice == "3":
            print("\nTransaction cancelled.")
            items.clear()
            prices.clear()
            for _, (_, items_list, prices_list) in category_data.items():
                items_list.clear()
                prices_list.clear()
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
        print("\nEnter: 'q' to quit, 'c' to checkout")
        item_name = input("Enter item name: ").strip()
        
        if item_name.lower() == "q":
            break
        elif item_name.lower() == "c":
            if items:
                if checkout_process(items, prices, category_data):
                    break
            else:
                print("Cart is empty. Please add items first.")
            continue
        
        if not item_name:
            print("Name cannot be empty.")
            continue
        
        try:
            price = float(input("Enter price: "))
            if price <= 0:
                print("Price must be greater than 0.")
                continue
        except ValueError:
            print("Invalid price. Please enter a number.")
            continue
        
        category = input("Enter category (f = food, c = clothing, e = electronics, p = pharmaceuticals): ").strip().lower()
        if category not in CATEGORIES:
            print("Invalid category. Use 'f', 'c', 'e', or 'p'.")
            continue
        
        category_name, items_list, prices_list = category_data[category]
        items_list.append(item_name)
        prices_list.append(price)
        items.append(item_name)
        prices.append(price)
        
        print(f"Added {item_name} (${price:.2f}) to {category_name}")
        print(f"Running total (without tax): ${sum(prices):.2f}")

if __name__ == "__main__":
    main()