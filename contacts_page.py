import csv
import io
import json
from pathlib import Path

import streamlit as st


DATA_FILE = Path(__file__).with_name("contacts.json")
CITIES = ["Київ", "Полтава", "Харків", "Львів", "Одеса", "Дніпро", "Інше"]


def load_contacts():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            contacts = json.load(file)
    except json.JSONDecodeError:
        return []

    if not isinstance(contacts, list):
        return []

    for index, contact in enumerate(contacts, start=1):
        contact.setdefault("id", index)
        contact.setdefault("notes", "")

    return contacts


def save_contacts(contacts):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(contacts, file, ensure_ascii=False, indent=2)


def make_contact_id(contacts):
    if not contacts:
        return 1

    ids = []
    for contact in contacts:
        ids.append(contact.get("id", 0))

    return max(ids) + 1


def make_contact(name, phone, email, city, notes, contacts):
    return {
        "id": make_contact_id(contacts),
        "name": name.strip(),
        "phone": phone.strip(),
        "email": email.strip(),
        "city": city,
        "notes": notes.strip(),
    }


def validate_contact(name, phone, email):
    if not name.strip():
        return "Введіть ім'я."

    if not phone.strip() or phone.strip() == "+380":
        return "Введіть телефон."

    if "@" not in email or "." not in email:
        return "Введіть коректний email."

    return ""


def filter_contacts(contacts, search_text, selected_city):
    result = []
    search_text = search_text.lower().strip()

    for contact in contacts:
        text = (
            contact.get("name", "")
            + " "
            + contact.get("phone", "")
            + " "
            + contact.get("email", "")
            + " "
            + contact.get("city", "")
            + " "
            + contact.get("notes", "")
        ).lower()

        search_ok = not search_text or search_text in text
        city_ok = selected_city == "Усі міста" or contact.get("city") == selected_city

        if search_ok and city_ok:
            result.append(contact)

    return result


def contact_label(contact):
    return f"{contact.get('name')} | {contact.get('phone')} | {contact.get('city')}"


def contacts_for_table(contacts):
    rows = []

    for contact in contacts:
        rows.append(
            {
                "ID": contact.get("id"),
                "Ім'я": contact.get("name"),
                "Телефон": contact.get("phone"),
                "Email": contact.get("email"),
                "Місто": contact.get("city"),
                "Коментар": contact.get("notes"),
            }
        )

    return rows


def contacts_to_csv(contacts):
    output = io.StringIO()
    fieldnames = ["id", "name", "phone", "email", "city", "notes"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()
    for contact in contacts:
        writer.writerow(
            {
                "id": contact.get("id", ""),
                "name": contact.get("name", ""),
                "phone": contact.get("phone", ""),
                "email": contact.get("email", ""),
                "city": contact.get("city", ""),
                "notes": contact.get("notes", ""),
            }
        )

    return output.getvalue()


def make_demo_contacts():
    return [
        {
            "id": 1,
            "name": "Олена Коваль",
            "phone": "+380501112233",
            "email": "olena@example.com",
            "city": "Київ",
            "notes": "Одногрупниця.",
        },
        {
            "id": 2,
            "name": "Максим Петренко",
            "phone": "+380671234567",
            "email": "maksym@example.com",
            "city": "Полтава",
            "notes": "Працює над фінальним проєктом.",
        },
        {
            "id": 3,
            "name": "Ірина Шевченко",
            "phone": "+380931112244",
            "email": "iryna@example.com",
            "city": "Львів",
            "notes": "Контакт для командної роботи.",
        },
    ]


def show_add_tab(contacts):
    with st.form("add_contact_form", clear_on_submit=True):
        st.subheader("Новий контакт")

        name = st.text_input("Ім'я")
        phone = st.text_input("Телефон", value="+380")
        email = st.text_input("Email")
        city = st.selectbox("Місто", CITIES)
        notes = st.text_area("Коментар")

        submitted = st.form_submit_button("Додати")

    if submitted:
        error = validate_contact(name, phone, email)
        if error:
            st.error(error)
            return

        contact = make_contact(name, phone, email, city, notes, contacts)
        contacts.append(contact)
        save_contacts(contacts)
        st.session_state.contacts = contacts
        st.success("Контакт збережено.")
        st.rerun()


def show_contacts_tab(filtered_contacts):
    if not filtered_contacts:
        st.info("Контактів не знайдено.")
        return

    st.dataframe(
        contacts_for_table(filtered_contacts),
        width="stretch",
        hide_index=True,
    )

    st.subheader("Деталі")
    for contact in filtered_contacts:
        with st.expander(contact_label(contact)):
            st.write(f"Ім'я: {contact.get('name')}")
            st.write(f"Телефон: {contact.get('phone')}")
            st.write(f"Email: {contact.get('email')}")
            st.write(f"Місто: {contact.get('city')}")
            st.write(f"Коментар: {contact.get('notes')}")


def show_delete_tab(contacts):
    if not contacts:
        st.info("Немає контактів для видалення.")
        return

    selected_contact = st.selectbox(
        "Оберіть контакт",
        contacts,
        format_func=contact_label,
    )

    if st.button("Видалити контакт"):
        contacts.remove(selected_contact)
        save_contacts(contacts)
        st.session_state.contacts = contacts
        st.success("Контакт видалено.")
        st.rerun()


def show_export_tab(contacts):
    st.download_button(
        "Завантажити CSV",
        contacts_to_csv(contacts),
        file_name="contacts.csv",
        mime="text/csv",
        disabled=not contacts,
    )

    if st.button("Показати JSON"):
        st.json(contacts)


def show_contacts_page():
    st.title("Список контактів")
    st.write("Міні-проєкт для збереження контактів у JSON та експорту у CSV.")

    if "contacts" not in st.session_state:
        st.session_state.contacts = load_contacts()

    contacts = st.session_state.contacts

    if not contacts:
        if st.button("Додати демо-контакти"):
            contacts = make_demo_contacts()
            save_contacts(contacts)
            st.session_state.contacts = contacts
            st.rerun()

    search_text = st.text_input("Пошук", placeholder="Ім'я, телефон, email або місто")
    city = st.selectbox("Місто", ["Усі міста"] + CITIES)
    filtered_contacts = filter_contacts(contacts, search_text, city)

    left, middle, right = st.columns(3)
    left.metric("Усього контактів", len(contacts))
    middle.metric("Знайдено", len(filtered_contacts))
    right.metric("Міст у списку", len({contact.get("city") for contact in contacts}))

    tab_add, tab_contacts, tab_delete, tab_export = st.tabs(
        ["Додати", "Контакти", "Видалити", "Експорт"]
    )

    with tab_add:
        show_add_tab(contacts)

    with tab_contacts:
        show_contacts_tab(filtered_contacts)

    with tab_delete:
        show_delete_tab(contacts)

    with tab_export:
        show_export_tab(contacts)
