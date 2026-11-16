import csv
from datetime import datetime
import os
import pandas as pd

FILE_NAME = "expenses.csv"


def initialize_csv():
    """Checks if the CSV file exists. If not, initializes it with headers."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Description", "Amount"])


def get_total_records():
    """Counts the number of data rows in the CSV file."""
    if not os.path.exists(FILE_NAME):
        return 0
    with open(FILE_NAME, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)
        return sum(1 for row in reader if row)


def add_expense():
    """Prompts user for input, validates it, and appends to the CSV file."""
    print("\n--- Add New Expense ---")
    date_input = input("Enter Date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date_input, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD. Expense not saved.")
        return

    category_input = input("Enter Category (e.g., Food, Travel): ").strip()
    if not category_input:
        print("Category cannot be empty. Expense not saved.")
        return

    description_input = input("Enter Description: ").strip()
    amount_raw = input("Enter Amount: ").strip()

    try:
        amount_input = float(amount_raw)
        if amount_input <= 0:
            print(
                "Invalid amount. Amount must be a positive number. Expense not"
                " saved."
            )
            return
    except ValueError:
        print(
            "Invalid amount. Amount must be a numerical value. Expense not"
            " saved."
        )
        return

    expense_record = {
        "Date": date_input,
        "Category": category_input,
        "Description": description_input,
        "Amount": amount_input,
    }

    with open(FILE_NAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["Date", "Category", "Description", "Amount"]
        )
        writer.writerow(expense_record)

    total_records = get_total_records()
    print(f"Expense saved. Total records: {total_records}")


def generate_category_summary():
    """Reads data using Pandas, processes aggregations, and prints the summary."""
    print("\n--- Category Summary ---")
    if get_total_records() == 0:
        print("No expenses recorded yet.")
        return

    df = pd.read_csv(FILE_NAME)
    category_totals = df.groupby("Category", sort=False)["Amount"].sum()
    grand_total = df["Amount"].sum()

    summary_parts = []
    for category, total in category_totals.items():
        display_total = int(total) if total.is_integer() else round(total, 2)
        summary_parts.append(f"{category}: {display_total}")

    display_grand_total = (
        int(grand_total) if grand_total.is_integer() else round(grand_total, 2)
    )
    print(" | ".join(summary_parts) + f" Total: {display_grand_total}")


def generate_monthly_summary():
    """Groups expenses by YYYY-MM using Pandas and prints monthly totals."""
    print("\n--- Monthly Summary ---")
    if get_total_records() == 0:
        print("No expenses recorded yet.")
        return

    df = pd.read_csv(FILE_NAME)
    df["Month"] = df["Date"].str.slice(0, 7)
    monthly_totals = df.groupby("Month")["Amount"].sum()

    summary_parts = []
    for month, total in monthly_totals.items():
        display_total = int(total) if total.is_integer() else round(total, 2)
        summary_parts.append(f"{month}: {display_total}")

    print(" | ".join(summary_parts))


def main():
    """Main application runtime loop."""
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
            if get_total_records() == 0:
                print("\nNo records found.")
            else:
                print("\n", pd.read_csv(FILE_NAME).to_string(index=False))
        elif choice == "3":
            generate_category_summary()
        elif choice == "4":
            generate_monthly_summary()
        elif choice == "5":
            print("\nExiting program. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select options 1 to 5.")


if __name__ == "__main__":
    main()
