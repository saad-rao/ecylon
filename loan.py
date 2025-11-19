import csv
import os
from datetime import datetime
import math

BASE_DIR = os.path.join(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DATA_DIR = os.path.abspath(DATA_DIR)

CLIENTS_FILE = os.path.join(DATA_DIR, "clients.csv")
LOANS_FILE = os.path.join(DATA_DIR, "loans.csv")


def generate_loan_id():
    # Uses LOANS_FILE for path checks
    if not os.path.isfile(LOANS_FILE):
        return "L001"
    with open(LOANS_FILE, "r") as f:
        reader = csv.DictReader(f)
        
        loan_ids = [row["Loan_ID"] for row in reader]
        if not loan_ids:
            return "L001"
        last_id = loan_ids[-1]
        new_id = "L" + str(int(last_id[1:]) + 1).zfill(3)
        return new_id



def read_clients():
    if not os.path.isfile(CLIENTS_FILE):
        print("No clients found.")
        return []
    clients = []
    with open(CLIENTS_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            
            cleaned_row = {k.strip(): v for k, v in row.items()}
            clients.append(cleaned_row)
    return clients


def select_client():
    clients = read_clients()
    if not clients:
        return None
    print("\n--- Clients List ---")
    for idx, client in enumerate(clients):
        
        print(f"{idx + 1}. {client['Name']} | CNIC: {client['CNIC']} | Risk: {client['Risk_level']}")

    try:
        choice = int(input("Select client by number: "))
        if 1 <= choice <= len(clients):
            return clients[choice - 1]
        else:
            print("Invalid selection number.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def calculate_monthly_installment(amount, duration):
    
    return round(amount / duration, 2)


def apply_loan():
    client = select_client()
    if not client:
        return

    loan_id = generate_loan_id()
    loan_type = input("Enter Loan Type (e.g., Personal, Business): ")

    try:
        amount = float(input("Enter Loan Amount: "))
        duration = int(input("Enter Duration (in months): "))
    except ValueError:
        print("Invalid input for Amount or Duration. Please enter numbers.")
        return

    start_date = input("Enter Start Date (YYYY-MM-DD): ")

    monthly_installment = calculate_monthly_installment(amount, duration)

    # Optional AI suggestion
    # Using 'Risk_level' key
    risk_level = client["Risk_level"]
    recommended_amount = amount
    if risk_level == "High":
        recommended_amount = min(amount, 50000)
        if recommended_amount < amount:
            print(f"⚠️ Risk Alert: Recommended max loan amount for high-risk client: {recommended_amount} PKR")
            # Ask the user if they want to proceed with the recommended amount
            use_recommended = input(f"Use recommended amount ({recommended_amount})? (y/n): ").lower()
            if use_recommended == 'y':
                amount = recommended_amount  # Update the amount used for saving
            else:
                print("Loan application cancelled.")
                return

    # Save loan
    # Uses LOANS_FILE for path checks
    file_exists = os.path.isfile(LOANS_FILE)
    with open(LOANS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            # CORRECTED HEADER: Added CNIC, Name, and fixed Risk_Level casing
            writer.writerow(["CNIC", "Name", "Loan_ID", "Loan_Type", "Loan_Amount", "Duration_Months", "Start_Date",
                             "Monthly_Installment", "Risk_level"])

        # Write the data row
        # Using 'Risk_level' key
        writer.writerow(
            [client["CNIC"], client["Name"], loan_id, loan_type, amount, duration, start_date, monthly_installment,
             risk_level])

    print(f"\nLoan {loan_id} created successfully for {client['Name']}!")
    print(f"Monthly installment: {monthly_installment} PKR")


def view_loans():
    # Uses LOANS_FILE for path checks
    if not os.path.isfile(LOANS_FILE):
        print("No loans found yet!")
        return
    print("\n--- Loans ---")
    with open(LOANS_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Using 'Risk_level' key
            print(
                f"Loan_ID: {row['Loan_ID']} | Name: {row['Name']} | Amount: {row['Loan_Amount']} | Installment: {row['Monthly_Installment']} | Start: {row['Start_Date']} | Duration: {row['Duration_Months']} months | Risk: {row['Risk_level']}")