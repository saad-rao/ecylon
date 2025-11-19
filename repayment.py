import csv
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DATA_DIR = os.path.abspath(DATA_DIR)

CLIENTS_FILE = os.path.join(DATA_DIR, "clients.csv")
LOANS_FILE = os.path.join(DATA_DIR, "loans.csv")
INSTALLMENTS_FILE = os.path.join(DATA_DIR, "installments.csv")
MODEL_FILE = os.path.join(DATA_DIR, "default_model.pkl")



def load_csv(filename):
    """Return rows from a CSV file as a list of dictionaries."""
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return list(csv.DictReader(f))


def get_client(cnic):
    """Return client data by CNIC."""
    clients = load_csv(CLIENTS_FILE)
    client = next((c for c in clients if c["CNIC"] == cnic), None)

    if not client:
        return ("Unknown", "Unknown", 0)

    # Uses 'Risk_level' key
    return (
        client["Name"],
        client["Risk_level"],
        float(client.get("Income", 0))
    )


if os.path.exists(MODEL_FILE):
    model = joblib.load(MODEL_FILE)
else:
    model = RandomForestClassifier()
    print("⚠ AI model not found — using default empty model.")


def view_schedule(loan_id):
    loans = load_csv(LOANS_FILE)
    installments = load_csv(INSTALLMENTS_FILE)

    loan = next((l for l in loans if l["Loan_ID"] == loan_id), None)

    if not loan:
        print("Loan not found!")
        return

    name, risk, income = get_client(loan["CNIC"])

    print(f"\nREPAYMENT SCHEDULE - {name} ({risk} Risk)")
    print(f"Loan: {loan['Loan_Amount']} PKR | {loan['Loan_Type']} | {loan['Duration_Months']} months")
    print("-" * 90)
    print(f"{'#':<4} {'Due Date':<12} {'Amount':<12} {'Status':<12} {'Paid On'}")
    print("-" * 90)

    loan_insts = [i for i in installments if i["Loan_ID"] == loan_id]

    overdue_count = 0
    consecutive_overdue = 0
    last_was_overdue = True

    for inst in sorted(loan_insts, key=lambda x: int(x["No"])):
        due = datetime.strptime(inst["Due_Date"], "%Y-%m-%d").date()
        status = inst["Status"]

        if status == "pending" and due < date.today():
            status = "OVERDUE"
            overdue_count += 1

            if last_was_overdue:
                consecutive_overdue += 1
        else:
            last_was_overdue = False

        print(
            f"{inst['No']:<4} {inst['Due_Date']:<12} {inst['Amount']} PKR   "
            f"{status:<12} {inst['Paid_Date']}"
        )



def show_alerts():
    print("\nDEFAULT & OVERDUE ALERTS")
    print("=" * 100)

    loans = load_csv(LOANS_FILE)
    installments = load_csv(INSTALLMENTS_FILE)

    alerts = []

    for loan in loans:
        name, risk, income = get_client(loan["CNIC"])
        loan_id = loan["Loan_ID"]

        loan_insts = [i for i in installments if i["Loan_ID"] == loan_id]

        overdue = sum(
            1 for i in loan_insts
            if i["Status"] == "pending"
            and datetime.strptime(i["Due_Date"], "%Y-%m-%d").date() < date.today()
        )

        # Skip low-risk if no overdue
        if overdue == 0 and risk != "High":
            continue

        consecutive = 0
        for i in sorted(loan_insts, key=lambda x: int(x["No"]), reverse=True):
            due = datetime.strptime(i["Due_Date"], "%Y-%m-%d").date()
            if i["Status"] == "paid" or due >= date.today():
                break
            consecutive += 1

        risk_num = {"Low": 0, "Medium": 1, "High": 2}.get(risk, 1)

        try:
            # NOTE: Model training/loading logic is outside this function and will need to be properly integrated
            # For now, it uses the fallback.
            prob = model.predict_proba([[overdue, consecutive, risk_num, income]])[0][1] * 100
        except:
            prob = overdue * 10  # fallback if model isn't trained

        alerts.append((prob, overdue, name, loan_id, risk))

    if not alerts:
        print("No alerts! All clients good.")
        return

    # Sort by highest risk
    for prob, overdue, name, lid, risk in sorted(alerts, reverse=True):
        status = "HIGH RISK" if prob >= 60 else "MONITORING"
        print(f"{status} → {name} | Overdue: {overdue} | AI Risk: {prob:.1f}% | Loan #{lid} | {risk}")