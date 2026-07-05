import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("budget_transactions.json")


def load_transactions():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return []

    if isinstance(data, list):
        return data

    return []


def save_transactions(transactions):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(transactions, file, ensure_ascii=False, indent=2)
