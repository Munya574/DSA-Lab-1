import csv
import uuid
import datetime

# Loan data (interest rates and max terms)
LOAN_OPTIONS = {
    "h": {"name": "Housing", "rate": 5.2, "max_term": 25},
    "a": {"name": "Auto", "rate": 7.5, "max_term": 6},
    "p": {"name": "Personal", "rate": 9.6, "max_term": 10},
}

def generate_unique_id():
    existing_ids = set()
    try:
        with open("loan_records.csv", "r") as file:
            reader = csv.reader(file)
            next(reader, None) 
            existing_ids = {row[0] for row in reader}
    except FileNotFoundError:
        pass
    
    while True:
        new_id = str(uuid.uuid4())[:8]
        if new_id not in existing_ids:
            return new_id

def get_current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Loan calculation function
def calculate_monthly_payment(principal, annual_rate, term_years):
    r = annual_rate / 100 / 12  # Monthly interest rate
    n = term_years * 12  # Total number of payments

    if r == 0:  # Handle zero-interest case
        return principal / n
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

# Validate loan term
def validate_term(loan_type, term):
    max_term = LOAN_OPTIONS[loan_type]["max_term"]
    return 1 <= term <= max_term

# Handle user input
def get_valid_input(prompt, cast_type, condition):
    while True:
        try:
            value = cast_type(input(prompt))
            if condition(value):
                return value
            print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid format. Enter a valid number.")
            
# Process loan

def process_loan():
    print("\n--- Welcome to Group 5's Bank Loan System ---\n")
    print("Loan Types: [H] Housing, [A] Auto, [P] Personal")
    
    loan_type = input("Enter loan type (H/A/P): ").strip().lower()
    while loan_type not in LOAN_OPTIONS:
        print("Invalid loan type. Choose from: H, A, or P.")
        loan_type = input("Enter loan type (H/A/P):  ").strip().lower()

    loan_name = LOAN_OPTIONS[loan_type]["name"]
    rate = LOAN_OPTIONS[loan_type]["rate"]
    max_term = LOAN_OPTIONS[loan_type]["max_term"]

    loan_amount = get_valid_input("Enter loan amount: $", float, lambda x: x > 0)
    term_years = get_valid_input(
        f"Enter loan term (1-{LOAN_OPTIONS[loan_type]['max_term']} years): ",
        int, lambda x: validate_term(loan_type, x)
    )
    monthly_income = get_valid_input("Enter your monthly income: ", float, lambda x: x > 0)

    monthly_payment = calculate_monthly_payment(loan_amount, rate, term_years)

    # Debt ratio check and adjustment
    while monthly_payment > monthly_income * 0.5:
        print("\n Sorry. Your monthly payment exceeds 50% of your income.")
        choice = input("Would you like to:\n1. Extend loan term (if possible)\n2. Enter a different loan amount\n3. Cancel loan application\nEnter choice (1/2/3): ").strip()
        
        if choice == "1" and term_years < max_term:
            term_years += 1
            monthly_payment = calculate_monthly_payment(loan_amount, rate, term_years)
            print(f"\nNew term: {term_years} years, New monthly payment: ${monthly_payment:.2f}")
        elif choice == "2":
            loan_amount = get_valid_input("Enter new loan amount: $", float, lambda x: x > 0)
            monthly_payment = calculate_monthly_payment(loan_amount, rate, term_years)
        elif choice == "3":
            print("\nYour loan application has been canceled.")
            return
        else:
            print("\nInvalid choice. Please try again.")
    
    loan_id = generate_unique_id()
    timestamp = get_current_timestamp()

    total_interest = (monthly_payment * term_years * 12) - loan_amount
    print("\n--- Loan Summary ---")
    print(f"Loan ID: {loan_id}")
    print(f"Loan Type: {loan_name}")
    print(f"Loan Amount: ${loan_amount:,.2f}")
    print(f"Interest Rate: {rate}%")
    print(f"Term: {term_years} years")
    print(f"Monthly Payment: ${monthly_payment:,.2f}")
    print(f"Total Interest Paid: ${total_interest:,.2f}")

    
    while True:
        confirm = input("\nWould you like to proceed with this loan? (Y/N): ").strip().lower()
        if confirm in ["y", "n"]:
            break
        print("\nInvalid input. Please enter Y or N.")
    
    if confirm != "y":
        print("\nLoan application canceled.")
        return
    
    # Store in CSV file
    file_exists = False
    try:
        with open("loan_records.csv", "r") as f:
            file_exists = bool(f.readline())
    except FileNotFoundError:
        pass

    with open("loan_records.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Loan ID", "Loan Type", "Amount", "Rate", "Term", "Monthly Payment", "Total Interest", "Timestamp", "Status"])
        writer.writerow([loan_id, loan_name, loan_amount, rate, term_years, monthly_payment, total_interest, timestamp, "Approved"])

    print("\n Your Loan has been APPROVED and recorded successfully!")

# Run the program
if __name__ == "__main__":
    process_loan()