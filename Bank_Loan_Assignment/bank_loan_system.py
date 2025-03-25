import csv

# Loan data (interest rates and max terms)
LOAN_OPTIONS = {
    "housing": {"rate": 5.2, "max_term": 25},
    "auto": {"rate": 7.5, "max_term": 6},
    "personal": {"rate": 9.6, "max_term": 10},
}

# Loan calculation function
def calculate_monthly_payment(principal, annual_rate, term_years):
    r = annual_rate / 100 / 12  # Monthly interest rate
    n = term_years * 12  # Total number of payments

    if r == 0:  # Handle zero-interest case
        return principal / n
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

# Function to validate loan term
def validate_term(loan_type, term):
    max_term = LOAN_OPTIONS[loan_type]["max_term"]
    return 1 <= term <= max_term

# Function to handle user input
def get_valid_input(prompt, cast_type, condition):
    while True:
        try:
            value = cast_type(input(prompt))
            if condition(value):
                return value
            print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid format. Enter a valid number.")

# Main loan processing function
def process_loan():
    print("\n--- Welcome to the Bank Loan System ---\n")
    print("Loan Types: Housing, Auto, Personal")
    
    loan_type = input("Enter loan type: ").strip().lower()
    while loan_type not in LOAN_OPTIONS:
        print("Invalid loan type. Choose from: Housing, Auto, Personal.")
        loan_type = input("Enter loan type: ").strip().lower()

    loan_amount = get_valid_input("Enter loan amount: ", float, lambda x: x > 0)
    term_years = get_valid_input(
        f"Enter loan term (1-{LOAN_OPTIONS[loan_type]['max_term']} years): ",
        int, lambda x: validate_term(loan_type, x)
    )
    monthly_income = get_valid_input("Enter your monthly income: ", float, lambda x: x > 0)

    rate = LOAN_OPTIONS[loan_type]["rate"]
    monthly_payment = calculate_monthly_payment(loan_amount, rate, term_years)

    # Debt ratio check
    if monthly_payment > monthly_income * 0.5:
        print("\n⚠ Warning: Your monthly payment exceeds 50% of your income.")
        print(f"Suggested lower amount or longer term (if available).")
        return
    
    total_interest = (monthly_payment * term_years * 12) - loan_amount
    print("\n--- Loan Summary ---")
    print(f"Loan Type: {loan_type.capitalize()}")
    print(f"Loan Amount: ${loan_amount:,.2f}")
    print(f"Interest Rate: {rate}%")
    print(f"Term: {term_years} years")
    print(f"Monthly Payment: ${monthly_payment:,.2f}")
    print(f"Total Interest Paid: ${total_interest:,.2f}")

    # Store in CSV file
    with open("loan_records.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([loan_type, loan_amount, rate, term_years, monthly_payment, total_interest, "Approved"])

    print("\n✅ Loan recorded successfully!")

# Run the program
if __name__ == "__main__":
    process_loan()
