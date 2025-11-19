import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DATA_DIR = os.path.abspath(DATA_DIR)

CLIENTS_FILE = os.path.join(DATA_DIR, "clients.csv")
STAFF_FILE = os.path.join(DATA_DIR, "staff.csv")

def validate_cnic(cnic):
    return cnic.isdigit() and len(cnic) == 13

def validation_phonenumber(phone):
    return phone.isdigit() and len(phone) == 11

def register_staff():
    print("\n Welcome to staff registration Portal\n")
    name = input("Enter your name: ")
    staff_id = input("Staff id: ")
    password = input("Password: ")

    file_exists = os.path.isfile(STAFF_FILE) 

    with open(STAFF_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Staff_ID", "Password"]) 
        writer.writerow([name, staff_id, password])
    print("Staff registered successfully!\n")

def risk_calculation(Clinet_onboarding):

    risk_score = 0
   
    if int(Clinet_onboarding["income"]) < 30000:
        risk_score += 20

    
    if Clinet_onboarding["phone"] == "":
        risk_score += 15

    if Clinet_onboarding["address"] == "":
        risk_score += 5

    if risk_score < 20:
        risk = "Low"
    elif risk_score < 40:
        risk = "Medium"
    else:
        risk = "High"

    return risk_score, risk


def Clinet_onboarding():
    print("\n Welcome to Client Onboarding Portal\n")
    print("Provide the details of the client\n")
    name = input("Client's fullname: ")
    address = input("Client's address: ")
    cnic = input("Client's CNIC: ")
    income = input("Client's monthly income: ")
    phone = input("Client's phone number: ")

    if not(validate_cnic(cnic)):
        print("Invalid CNIC Format")
        return
    if not(validation_phonenumber(phone)):
        print("Invalid Phone Number or wrong format")
        return

    clients_information = {
        "name": name,
        "address": address,
        "cnic": cnic,
        "income": income,
        "phone": phone
    }
    risk_score, risk = risk_calculation(clients_information)
    clients_information["risk"] = risk
    clientdata_csv(clients_information)
    print("\n Client Onboarding Complete")
    print("Client registered successfully")
    print(f"\nRisk level: {risk}\n")

def clientdata_csv(Clinet_onboarding):

    file_exists = os.path.isfile(CLIENTS_FILE) # FIX: Use CLIENTS_FILE variable

    with open(CLIENTS_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "Name", "Address", "Phone", "CNIC", "Income", "Risk_level"
            ])

        writer.writerow([
            Clinet_onboarding["name"],
            Clinet_onboarding["address"],
            Clinet_onboarding["phone"],
            Clinet_onboarding["cnic"],
            Clinet_onboarding["income"],
            Clinet_onboarding["risk"]
        ])

def client_searching():
    print("\n SEARCHING CLIENT ")
    cnic = input("Enter CNIC to search: ")

    if not validate_cnic(cnic):
        print("Invalid CNIC format.")
        return

    if not os.path.isfile(CLIENTS_FILE): # FIX: Use CLIENTS_FILE variable
        print("No client data found yet!")
        return

    flag = False
    with open(CLIENTS_FILE, "r") as f: # FIX: Use CLIENTS_FILE variable
        reader = csv.DictReader(f)
        # print("CSV Columns found:", reader.fieldnames) # Debug line removed

        for row in reader:
            if row.get("CNIC") == cnic:
                flag = True
                print("\n--- CLIENT FOUND ---")
                print(f"Name: {row.get('Name')}")
                print(f"Address: {row.get('Address')}")
                print(f"Phone: {row.get('Phone')}")
                print(f"Income: {row.get('Income')}")
                print(f"Risk Level: {row.get('Risk_level')}\n")
                break

    if not flag:
        print("No client is registered with this CNIC number\n")