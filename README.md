# Receipt Management System

## Overview  
A Python-based CLI application for handling purchases, calculating taxes, generating receipts, and managing transactions.  
It allows users to add items to a shopping cart, categorize them, calculate totals with tax, and save receipts as text files.  

## Features  
- **Item Categorization**: Supports Food, Clothing, Electronics, and Pharmaceuticals.  
- **Tax Calculation**: Automatically calculates tax (10.44%) for each item.  
- **Cart Management**: Add, remove, and list items in the cart.  
- **Receipt Generation**: Creates a detailed receipt with itemized categories and tax breakdown.  
- **Transaction ID Handling**: Ensures unique transaction IDs for each purchase.  
- **Persistent Storage**: Saves receipts as text files in a "receipts" directory.  

## Installation & Usage  
### Prerequisites  
- Python 3.x  

### Running the Program  
```sh
python main.py
```

### Commands  
- **Enter item name** → Add an item to the cart.  
- **Enter price** → Assign a price to the item.  
- **Select category** → Choose from (f = Food, c = Clothing, e = Electronics, p = Pharmaceuticals).  
- **c** → Checkout and generate a receipt.  
- **q** → Quit without checkout.  

## File Structure  
```
receipt_system/
│-- main.py         # Main program file
│-- receipts/       # Directory where receipts are saved
```

## License  
This project is open-source and available for modification and use.  
