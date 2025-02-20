import json
import os

def calculate_tax(price):
    tax_rate = 10.44 / 100
    return price * tax_rate

def display_category_items(category_name, items, prices):
    if items:
        print(f"\n{category_name}:")
        print("{:<25} {:>12}".format("Item", "Price ($)"))
        print("-" * 40)
        for i, (item, price) in enumerate(zip(items, prices)):
            print(f"{i}. {item:<25} ${price:>9.2f}")

def generate_receipt_data(items, prices, food, food_prices, clothing, clothing_prices, electronics, electronics_prices, pharmaceuticals, pharmaceuticals_prices):
    # Calculate totals
    total_before_tax = sum(prices)
    total_tax = sum(calculate_tax(price) for price in prices)
    total_after_tax = total_before_tax + total_tax
    
    # Create categories dictionary with items and prices
    categories = {
        "food": [{"item": item, "price": price} for item, price in zip(food, food_prices)],
        "clothing": [{"item": item, "price": price} for item, price in zip(clothing, clothing_prices)],
        "electronics": [{"item": item, "price": price} for item, price in zip(electronics, electronics_prices)],
        "pharmaceuticals": [{"item": item, "price": price} for item, price in zip(pharmaceuticals, pharmaceuticals_prices)]
    }
    
    # Create receipt data structure
    receipt_data = {
        "items": [{"name": item, "price": price} for item, price in zip(items, prices)],
        "categories": categories,
        "subtotal": total_before_tax,
        "tax": total_tax,
        "total": total_after_tax
    }
    
    return receipt_data

def save_receipt_to_json(receipt_data):
    """Saves the receipt data to receipts.json and confirm to the user."""

    file_name = "receipts.json"

    # Check if file exists, if not create it
    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            json.dump([], file)

    # Read existing data
    with open(file_name, "r") as file:
        receipts = json.load(file)

    # Add new receipt and save
    receipts.append(receipt_data)

    with open(file_name, "w") as file:
        json.dump(receipts, file, indent=4)

    print("\n Your receipt has been saved!")

def checkout_process(items, prices, food, food_prices, clothing, clothing_prices, electronics, electronics_prices, pharmaceuticals, pharmaceuticals_prices):
    while True:
        total_before_tax = sum(prices)
        total_tax = sum(calculate_tax(price) for price in prices)
        total_after_tax = total_before_tax + total_tax

        # Header
        print("\n" + "=" * 40)
        print("{:^40}".format("SHOPPING CART"))
        print("=" * 40)

        # Display categories
        display_category_items("Food", food, food_prices)
        display_category_items("Clothing", clothing, clothing_prices)
        display_category_items("Electronics", electronics, electronics_prices)
        display_category_items("Pharmaceuticals", pharmaceuticals, pharmaceuticals_prices)

        # Display totals
        print("\n" + "-" * 40)
        print("{:<25} ${:>9.2f}".format("Subtotal:", total_before_tax))
        print("{:<25} ${:>9.2f}".format("Tax:", total_tax))
        print("{:<25} ${:>9.2f}".format("Total:", total_after_tax))
        print("=" * 40)

        # User choice
        print("\nOptions:")
        print("1. Complete Checkout")
        print("2. Remove Item")
        print("3. Cancel Transaction")
        
        choice = input("\nEnter choice (1/2/3): ").strip()

        if choice == "1":

            receipt_data = generate_receipt_data(
                items, prices, food, food_prices, clothing, 
                clothing_prices, electronics, electronics_prices, 
                pharmaceuticals, pharmaceuticals_prices
            )
            save_receipt_to_json(receipt_data)

            print("\nCheckout complete! Thank you for shopping!")
            return True

        elif choice == "2":
            if not items:
                print("\nNo items to remove.")
                continue
                
            try:
                remove_index = int(input(f"Enter item number (1-{len(items)}): ")) - 1 # convert to 0-based index
                if 0 <= remove_index < len(items): 
                    item_to_remove = items[remove_index]
                    
                    # Remove from main lists
                    removed_item = items.pop(remove_index)
                    removed_price = prices.pop(remove_index)
                    
                    # Remove from category lists
                    if item_to_remove in food:
                        idx = food.index(item_to_remove)
                        food.pop(idx)
                        food_prices.pop(idx)
                    elif item_to_remove in clothing:
                        idx = clothing.index(item_to_remove)
                        clothing.pop(idx)
                        clothing_prices.pop(idx)
                    elif item_to_remove in electronics:
                        idx = electronics.index(item_to_remove)
                        electronics.pop(idx)
                        electronics_prices.pop(idx)
                    elif item_to_remove in pharmaceuticals:
                        idx = pharmaceuticals.index(item_to_remove)
                        pharmaceuticals.pop(idx)
                        pharmaceuticals_prices.pop(idx)

                    print(f"\nRemoved {removed_item} (${removed_price:.2f})")
                else:
                    print("\nInvalid item number. Please try again.")
            except ValueError:
                print("\nInvalid input. Please enter a number.")

        elif choice == "3":
            print("\nTransaction cancelled.")
            items.clear()
            prices.clear()
            return False

        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")

def main():
    item = []
    prices =[]
    food = []
    clothing = []
    electronics = []
    pharmaceuticals = []
    food_prices = []
    clothing_prices = []
    electronics_prices = []
    pharmaceuticals_prices = []

    while True:
        item_name = input('Enter item name (input "q" to quit or "c" to checkout): ').strip()

        if item_name.lower() == "q":
            break
        elif item_name.lower() == "c":
            if item:
                if checkout_process(item, prices, food, food_prices, clothing, clothing_prices, electronics, electronics_prices, pharmaceuticals, pharmaceuticals_prices):
                    break
            else:
                print("Cart is empty. Please add items first.")
            continue

        if not item_name:
            print("Name cannot be empty. Please enter an item name.")
            continue

        try:
            price = float(input('Enter price: '))
            if price <= 0:
                print("Price must be greater than 0. Re-enter item name and price")
                continue
                    
            while True:
                category = input("Enter category (f = food/ c = clothing/ e = electronics/ p = pharmaceuticals): ").strip().lower()
                if category in ["f", "c", "e", "p"]:
                    break
                print("Invalid category. Please enter 'f', 'c', 'e', or 'p'.")

            if category == "f":
                food.append(item_name)
                food_prices.append(price)
            elif category == "c":
                clothing.append(item_name)
                clothing_prices.append(price)
            elif category == "e":
                electronics.append(item_name)
                electronics_prices.append(price)
            elif category == "p":
                pharmaceuticals.append(item_name)
                pharmaceuticals_prices.append(price)

            item.append(item_name)
            prices.append(price)

            print(f"Item added! Running total (without tax): ${sum(prices):.2f}")

        except ValueError:
            print("Invalid input. Re-enter item name and price")

if __name__ == "__main__":
    main()