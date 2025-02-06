def calculate_tax(price):
    tax_rate = 10.44 / 100
    return price * tax_rate

def checkout_process(items, prices):
    while True:
        # totals
        total_before_tax = sum(prices)
        total_tax = sum(calculate_tax(price) for price in prices)
        total_after_tax = total_before_tax + total_tax
        #remaining_balance = max_total - total_after_tax

        # header
        print("\n" + "=" * 40)
        print("{:^40}".format("SHOPPING CART"))
        print("=" * 40)

        if not items:
            print("\nCart is empty. No items to checkout.")
            return False

        # Display items
        print("\n{:<25} {:>12}".format("Item", "Price ($)")) 
        print("-" * 40)
        for i, (item, price) in enumerate(zip(items, prices), 1): 
            print(f"{i}. {item:<22} ${price:>9.2f}")

        # Display totals
        print("\n" + "-" * 40)
        print("{:<25} ${:>9.2f}".format("Subtotal:", total_before_tax))
        print("{:<25} ${:>9.2f}".format("Tax:", total_tax))
        print("{:<25} ${:>9.2f}".format("Total:", total_after_tax))
        #print("{:<25} ${:>9.2f}".format("Remaining Balance:", remaining_balance))

        print("=" * 40)

        # User choice
        print("\nOptions:")
        print("1. Complete Checkout")
        print("2. Remove Item")
        print("3. Cancel Transaction")
        
        try:
            choice = input("\nEnter choice (1/2/3): ").strip()

            if choice == "1":
                #if remaining_balance < 0:
                    #print("\nCannot checkout: Total exceeds maximum limit")
                    #continue
                print("\nCheckout complete! Thank you for shopping!")
                return True

            elif choice == "2":
                if not items:
                    print("\nNo items to remove.")
                    continue
                    
                try:
                    remove_index = int(input(f"Enter item number (1-{len(items)}): ")) - 1 # covert to 0-based index
                    if 0 <= remove_index < len(items): 
                        removed_item = items.pop(remove_index) # remove item and price at index
                        removed_price = prices.pop(remove_index)
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

        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again.")

def main():
    item = []
    prices =[]
    food = []
    clothing = []
    electronics = []
    pharmaceuticals = []
    #max_total = 100
    running_total = 0

    while True:
        item_name = input('Enter item name (input "q" to quit or "c" to checkout): ')

        if item_name.lower() == "q":
            break
        elif item_name.lower() == "c":
            if item:
                checkout_process(item, prices)
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
                
            tax = calculate_tax(price)
            total_with_tax = price + tax
            
            #if running_total + total_with_tax > max_total:
            #    print(f"Adding this item would exceed your ${max_total} limit. Remaining balance: ${max_total - running_total:.2f}")
             #   continue
        
            category = input("Enter category (F = food/ c = clothing/ e = electronics/ p = pharmaceuticals): ")
            if category.lower() == "f":
                food.append(item_name)
            elif category.lower() == "c":
                clothing.append(item_name)
            elif category.lower() == "e":
                electronics.append(item_name)
            elif category.lower() == "p":
                pharmaceuticals.append(item_name)

            item.append(item_name)
            prices.append(price)
            running_total += total_with_tax
            print(f"Item added! Running total (with tax): ${running_total:.2f}")
            # print(f"Remaining balance: ${max_total - running_total:.2f}")

        except ValueError:
            print(" Invalid input. Re-enter item name and price")

if __name__ == "__main__":
    main()
