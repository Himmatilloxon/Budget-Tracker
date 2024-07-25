from expense import *
import calendar
import datetime

def main():
    print("Running Expense Tracker!")
    expense_file_path = "expense.csv"
    budget = 10000

    # Get user expense
    expense = get_user_expense()

    # Save expense to file
    save_expense_to_file(expense, expense_file_path)

    # Summarize expense
    summarize_expense(expense_file_path, budget)

def get_user_expense() -> Expense:
    print("Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    print(f"You've entered {expense_name}, {expense_amount}")

    expense_categories = ["Food", "Home", "Work", "Study", "Sport", "Fun"]
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(expense_name, selected_category, expense_amount)
            return new_expense
        else:
            print("Invalid category. Please try again!")

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name}, {expense.amount}, {expense.category}\n")

def summarize_expense(expense_file_path, budget):
    print("Summarizing User Expense")
    expenses: list[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(", ")
            if len(line) != 3: continue
            expense_name, expense_amount, expense_category = line

            line_expense = Expense(name = expense_name, amount = float(expense_amount), category = expense_category)
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("\nExpenses By Category: ")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    total_spent = sum([e.amount for e in expenses])
    print()
    print(red(f"Total Spent: ${total_spent:.2f}"))

    remaining_budget = budget - total_spent
    print(blue(f"--> Budget Remaining: ${remaining_budget:.2f}"))

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    if remaining_days > 0:
        daily_budget = remaining_budget / remaining_days
        print(green(f">>> Budget Per Day: ${daily_budget:.2f}"))
    else:
        print(red("No remaining days in the month to calculate daily budget!"))

def green(text):
    return f"\033[92m{text}\033[0m"

def red(text):
    return f"\033[91m{text}\033[0m"

def blue(text):
    return f"\033[94m{text}\033[0m"

if __name__ == "__main__":
    main()