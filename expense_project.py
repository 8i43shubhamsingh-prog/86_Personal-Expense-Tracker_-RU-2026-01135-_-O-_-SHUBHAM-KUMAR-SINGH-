import csv
import os
from datetime import datetime
import pandas as pd

FILENAME = "expenses.csv"
FIELDNAMES = ["Date", "Category", "Description", "Amount"]


def initialize_csv():
    """Creates expenses.csv with headers if it does not exist."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_expenses():
    """Reads all records from expenses.csv into a list of dictionaries."""
    initialize_csv()
    expenses = []
    with open(FILENAME, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["Amount"] = float(row["Amount"])
            expenses.append(row)
    return expenses


def validate_date(date_str):
    """Validates YYYY-MM-DD date format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_amount(amount_str):
    """Validates that amount is a positive number (>= 1 or > 0)."""
    try:
        amount = float(amount_str)
        if amount <= 0:
            return None
        return amount
    except ValueError:
        return None


def add_expense():
    """Prompts for expense details, validates them, and saves to expenses.csv."""
    print("\n--- Add New Expense ---")
    first_input = input("Enter Date (YYYY-MM-DD): ").strip()

    # Supports both comma-separated single line (Test Cases 1-3) and separate prompts
    if "," in first_input:
        parts = [item.strip() for item in first_input.split(",")]
        if len(parts) != 4:
            print("Invalid input format. Expense not saved.")
            return
        date_str, category, description, amount_str = parts
    else:
        date_str = first_input
        category = input("Enter Category (e.g., Food, Travel): ").strip()
        description = input("Enter Description: ").strip()
        amount_str = input("Enter Amount: ").strip()

    if not validate_date(date_str):
        print("Invalid date format. Please use YYYY-MM-DD. Expense not saved.")
        return

    if not category:
        print("Category cannot be empty. Expense not saved.")
        return

    if not description:
        print("Description cannot be empty. Expense not saved.")
        return

    amount = validate_amount(amount_str)
    if amount is None:
        print("Invalid amount. Amount must be a positive number. Expense not saved.")
        return

    clean_amount = int(amount) if amount.is_integer() else amount

    record = {
        "Date": date_str,
        "Category": category,
        "Description": description,
        "Amount": clean_amount,
    }

    initialize_csv()
    with open(FILENAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(record)

    total_records = len(load_expenses())
    print(f"Expense saved. Total records: {total_records}")


def view_all_records():
    """Displays all records from expenses.csv."""
    expenses = load_expenses()
    if not expenses:
        print("\nNo records found.")
        return

    print("\n--- All Expense Records ---")
    for idx, exp in enumerate(expenses, start=1):
        amt = int(exp["Amount"]) if exp["Amount"].is_integer() else exp["Amount"]
        print(f"{idx}. {exp['Date']} | {exp['Category']} | {exp['Description']} | {amt}")


def view_category_summary():
    """Displays category-wise summary using Pandas groupby()."""
    initialize_csv()
    df = pd.read_csv(FILENAME)

    if df.empty:
        print("\nNo records found.")
        return

    grouped = df.groupby("Category", sort=False)["Amount"].sum()
    parts = []

    for category, total in grouped.items():
        clean_total = int(total) if float(total).is_integer() else round(total, 2)
        parts.append(f"{category}: {clean_total}")

    grand_total = df["Amount"].sum()
    clean_grand = int(grand_total) if float(grand_total).is_integer() else round(grand_total, 2)

    print(" | ".join(parts))
    print(f"Total: {clean_grand}")


def view_monthly_summary():
    """Displays monthly summary using Pandas groupby()."""
    initialize_csv()
    df = pd.read_csv(FILENAME)

    if df.empty:
        print("\nNo records found.")
        return

    print("\n--- Monthly Summary ---")
    df["Month"] = pd.to_datetime(df["Date"]).dt.to_period("M")
    grouped = df.groupby("Month")["Amount"].sum()

    for month, total in grouped.items():
        clean_total = int(total) if float(total).is_integer() else round(total, 2)
        print(f"{month}: {clean_total}")


def main():
    initialize_csv()
    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View All Records (Raw View)")
        print("3. View Category Summary")
        print("4. View Monthly Summary")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_all_records()
        elif choice == "3":
            view_category_summary()
        elif choice == "4":
            view_monthly_summary()
        elif choice == "5":
            print("Exiting Personal Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid option. Please select between 1 and 5.")


if __name__ == "__main__":
    main()
