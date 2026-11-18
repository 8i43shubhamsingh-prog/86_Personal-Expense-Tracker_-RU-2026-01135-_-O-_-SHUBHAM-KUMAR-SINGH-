# 86_Personal-Expense-Tracker_<RU-2026-01135>_<O>_<SHUBHAM KUMAR SINGH>

Personal Expense Tracker

A simple Python console app to record daily expenses, save them in a CSV file, and view spending summaries.

Features

• Add daily expenses (Date, Category, Description, Amount)
• Validates date format (YYYY-MM-DD) and checks that amount is positive
• Saves all data automatically in expenses.csv
• View all saved expenses
• Category-wise and monthly spending summaries using Pandas

Requirements

• Python 3
• Pandas library (pip install pandas)

How to Run

1. Open terminal in the project folder.
2. Run: python expense_project.py
3. Follow the menu options (1 to 5).

Test Cases

• Normal Input: 2026-08-10, Food, Lunch, 250 -> Expense saved. Total records: 1
• Minimum Input: 2026-08-10, Travel, Bus, 1 -> Expense saved. Total records: 1
• Invalid Input: 2026-08-10, Food, Tea, -50 -> Invalid amount. Amount must be a positive number. Expense not saved.
• Category Summary: Food: 400 | Travel: 100 and Total: 500

