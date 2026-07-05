import csv
import io
from datetime import date


TRANSACTION_TYPES = ["expense", "income"]

TYPE_LABELS = {
    "expense": "Витрата",
    "income": "Дохід",
}

EXPENSE_CATEGORIES = [
    "Їжа",
    "Транспорт",
    "Навчання",
    "Здоров'я",
    "Розваги",
    "Покупки",
    "Інше",
]

INCOME_CATEGORIES = [
    "Стипендія",
    "Підробіток",
    "Подарунок",
    "Фриланс",
    "Інше",
]


def make_transaction_id(transactions):
    if not transactions:
        return 1

    ids = []
    for transaction in transactions:
        ids.append(transaction.get("id", 0))

    return max(ids) + 1


def add_transaction(transactions, transaction):
    transactions.append(transaction)
    return transactions


def delete_transaction(transactions, transaction_id):
    result = []

    for transaction in transactions:
        if transaction.get("id") != transaction_id:
            result.append(transaction)

    return result


def get_categories(transaction_type):
    if transaction_type == "income":
        return INCOME_CATEGORIES

    return EXPENSE_CATEGORIES


def calculate_summary(transactions):
    income = 0
    expenses = 0

    for transaction in transactions:
        amount = float(transaction.get("amount", 0))

        if transaction.get("type") == "income":
            income += amount
        else:
            expenses += amount

    return {
        "income": income,
        "expenses": expenses,
        "balance": income - expenses,
    }


def filter_transactions(transactions, transaction_type, category, search_text):
    filtered = []
    search_text = search_text.lower().strip()

    for transaction in transactions:
        type_ok = transaction_type == "Усі" or transaction.get("type") == transaction_type
        category_ok = category == "Усі" or transaction.get("category") == category

        text = " ".join(
            [
                transaction.get("category", ""),
                transaction.get("comment", ""),
                transaction.get("date", ""),
            ]
        ).lower()
        search_ok = not search_text or search_text in text

        if type_ok and category_ok and search_ok:
            filtered.append(transaction)

    return filtered


def count_expenses_by_category(transactions):
    result = {}

    for transaction in transactions:
        if transaction.get("type") != "expense":
            continue

        category = transaction.get("category", "Інше")
        amount = float(transaction.get("amount", 0))
        result[category] = result.get(category, 0) + amount

    return result


def transactions_to_csv(transactions):
    headers = ["id", "date", "type", "category", "amount", "comment"]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)

    writer.writeheader()
    for transaction in transactions:
        writer.writerow(
            {
                "id": transaction.get("id", ""),
                "date": transaction.get("date", ""),
                "type": transaction.get("type", ""),
                "category": transaction.get("category", ""),
                "amount": transaction.get("amount", ""),
                "comment": transaction.get("comment", ""),
            }
        )

    return output.getvalue()


def make_demo_transactions():
    return [
        {
            "id": 1,
            "date": str(date.today()),
            "type": "income",
            "category": "Підробіток",
            "amount": 2500.0,
            "comment": "Оплата за невелике завдання",
        },
        {
            "id": 2,
            "date": str(date.today()),
            "type": "expense",
            "category": "Їжа",
            "amount": 320.0,
            "comment": "Обід і продукти",
        },
        {
            "id": 3,
            "date": str(date.today()),
            "type": "expense",
            "category": "Навчання",
            "amount": 450.0,
            "comment": "Книга або курс",
        },
    ]
