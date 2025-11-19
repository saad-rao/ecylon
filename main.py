from clients import Clinet_onboarding, client_searching, register_staff
from loan import apply_loan, view_loans

def main():
    while True:
        print("\n--- Microfinance Loan Management System ---")
        print("1. Register Staff")
        print("2. Register Client")
        print("3. Search Client")
        print("4. Apply Loan")
        print("5. View Loans")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            register_staff()
        elif choice == "2":
            Clinet_onboarding()
        elif choice == "3":
            client_searching()
        elif choice == "4":
            apply_loan()
        elif choice == "5":
            view_loans()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()