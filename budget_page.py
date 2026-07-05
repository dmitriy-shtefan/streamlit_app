from datetime import date

import streamlit as st

from budget_logic import (
    EXPENSE_CATEGORIES,
    INCOME_CATEGORIES,
    TRANSACTION_TYPES,
    TYPE_LABELS,
    add_transaction,
    calculate_summary,
    count_expenses_by_category,
    delete_transaction,
    filter_transactions,
    get_categories,
    make_demo_transactions,
    make_transaction_id,
    transactions_to_csv,
)
from storage import load_transactions, save_transactions


def prepare_table(transactions):
    rows = []

    for transaction in transactions:
        rows.append(
            {
                "Дата": transaction.get("date"),
                "Тип": TYPE_LABELS.get(transaction.get("type"), transaction.get("type")),
                "Категорія": transaction.get("category"),
                "Сума": transaction.get("amount"),
                "Коментар": transaction.get("comment"),
            }
        )

    return rows


def show_summary(transactions):
    summary = calculate_summary(transactions)

    first, second, third = st.columns(3)
    first.metric("Доходи", f"{summary['income']:.2f} грн")
    second.metric("Витрати", f"{summary['expenses']:.2f} грн")
    third.metric("Баланс", f"{summary['balance']:.2f} грн")

    if summary["balance"] < 0:
        st.warning("Витрати більші за доходи. Варто переглянути категорії витрат.")
    elif summary["balance"] == 0:
        st.info("Баланс дорівнює нулю. Додай доходи або витрати для аналізу.")
    else:
        st.success("Баланс позитивний. Є простір для заощаджень.")


def show_add_form(transactions):
    with st.form("add_transaction_form", clear_on_submit=True):
        st.subheader("Додати запис")

        transaction_type = st.selectbox(
            "Тип",
            TRANSACTION_TYPES,
            format_func=lambda value: TYPE_LABELS[value],
        )
        category = st.selectbox("Категорія", get_categories(transaction_type))

        col_one, col_two = st.columns(2)
        with col_one:
            amount = st.number_input("Сума, грн", min_value=0.0, step=10.0)
        with col_two:
            transaction_date = st.date_input("Дата", value=date.today())

        comment = st.text_input("Коментар")

        submitted = st.form_submit_button("Зберегти")

        if submitted:
            if amount <= 0:
                st.error("Сума має бути більшою за нуль.")
                return

            transaction = {
                "id": make_transaction_id(transactions),
                "date": str(transaction_date),
                "type": transaction_type,
                "category": category,
                "amount": float(amount),
                "comment": comment.strip(),
            }

            st.session_state.transactions = add_transaction(transactions, transaction)
            save_transactions(st.session_state.transactions)
            st.success("Запис збережено.")
            st.rerun()


def show_filters():
    categories = ["Усі"]
    for category in EXPENSE_CATEGORIES + INCOME_CATEGORIES:
        if category not in categories:
            categories.append(category)

    filter_one, filter_two, filter_three = st.columns(3)

    with filter_one:
        transaction_type = st.selectbox(
            "Фільтр за типом",
            ["Усі"] + TRANSACTION_TYPES,
            format_func=lambda value: value if value == "Усі" else TYPE_LABELS[value],
        )

    with filter_two:
        category = st.selectbox("Фільтр за категорією", categories)

    with filter_three:
        search_text = st.text_input("Пошук у коментарях")

    return transaction_type, category, search_text


def show_expense_chart(transactions):
    category_totals = count_expenses_by_category(transactions)

    if not category_totals:
        st.info("Ще немає витрат для графіка.")
        return

    chart_data = []
    for category, amount in category_totals.items():
        chart_data.append({"Категорія": category, "Сума": amount})

    st.bar_chart(chart_data, x="Категорія", y="Сума")


def show_transaction_list(filtered_transactions, all_transactions):
    if not filtered_transactions:
        st.info("Записів поки немає.")
        return

    st.dataframe(prepare_table(filtered_transactions), use_container_width=True)

    st.subheader("Видалення запису")
    selected_id = st.selectbox(
        "Обери запис",
        [transaction["id"] for transaction in filtered_transactions],
        format_func=lambda transaction_id: describe_transaction(filtered_transactions, transaction_id),
    )

    if st.button("Видалити запис"):
        st.session_state.transactions = delete_transaction(all_transactions, selected_id)
        save_transactions(st.session_state.transactions)
        st.success("Запис видалено.")
        st.rerun()


def describe_transaction(transactions, transaction_id):
    for transaction in transactions:
        if transaction.get("id") == transaction_id:
            label = TYPE_LABELS.get(transaction.get("type"), transaction.get("type"))
            return (
                f"{transaction.get('date')} | {label} | "
                f"{transaction.get('category')} | {transaction.get('amount')} грн"
            )

    return str(transaction_id)


def show_export(transactions):
    st.download_button(
        "Завантажити CSV",
        transactions_to_csv(transactions),
        file_name="budget_transactions.csv",
        mime="text/csv",
        disabled=not transactions,
    )


def show_budget_page():
    st.title("Personal Budget Tracker")
    st.write(
        "Міні-застосунок для обліку доходів і витрат. "
        "Це перший проєкт, який студент може показати у своєму портфоліо."
    )

    if "transactions" not in st.session_state:
        st.session_state.transactions = load_transactions()

    transactions = st.session_state.transactions

    if not transactions:
        if st.button("Додати демо-дані"):
            st.session_state.transactions = make_demo_transactions()
            save_transactions(st.session_state.transactions)
            st.rerun()

    show_summary(transactions)

    tab_add, tab_history, tab_analysis, tab_export = st.tabs(
        ["Додати", "Історія", "Аналіз", "Експорт"]
    )

    with tab_add:
        show_add_form(transactions)

    with tab_history:
        transaction_type, category, search_text = show_filters()
        filtered_transactions = filter_transactions(
            transactions,
            transaction_type,
            category,
            search_text,
        )
        show_transaction_list(filtered_transactions, transactions)

    with tab_analysis:
        st.subheader("Витрати за категоріями")
        show_expense_chart(transactions)

    with tab_export:
        show_export(transactions)
