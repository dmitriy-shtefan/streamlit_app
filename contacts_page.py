import time
import streamlit as st
import pandas as pd
from files_db import load_contacts, save_contacts, make_contact_id
from validation import validate_email, validate_phone


CITIES = ('Київ', 'Полтава', 'Харків', 'Львів', 'Одеса', 'Дніпро')


def display_contacts(contacts):
    for contact in contacts:
        with st.expander(contact['name']):
            st.write(f"ID: {contact.get('id', 'N/A')}")
            st.write(f"Ім'я: {contact['name']}")
            st.write(f"Телефон: {contact['phone']}")
            st.write(f"Email: {contact['email']}")
            st.write(f"Місто: {contact['city']}")
            # contact.get('sex', 'N/A')
            # contact['sex']


def display_contacts_tabular(contacts):
    df = pd.DataFrame(contacts)
    st.dataframe(df, hide_index=True)


def get_contact_form_data(contacts):
    with st.form("contact_form"):
        st.subheader("Новий контакт")

        name = st.text_input(f"Ім'я:", placeholder="Введіть ваше ім'я").strip()
        phone = st.text_input(f"Телефон:", "+380").strip()
        email = st.text_input(f"Email:", placeholder="Введіть ваш email").strip()
        city = st.selectbox(f"Місто:", CITIES)

        submitted = st.form_submit_button("Додати й зберегти")

    if submitted:
        phone_ok, phone_message = validate_phone(phone)
        email_ok, email_message = validate_email(email)

        if not name:
            return False, "Ім'я не має бути порожнім.", {}

        if not phone_ok:
            return False, phone_message, {}

        if not email_ok:
            return False, email_message, {}

        contact = {
            "id": make_contact_id(contacts),
            "name": name,
            "phone": phone,
            "email": email,
            "city": city
        }
        return True, "", contact

    return False, "", {}


def delete_contact_by_id(contacts, contact_id):
    updated_contacts = []

    for contact in contacts:
        if contact.get("id") != contact_id:
            updated_contacts.append(contact)

    return updated_contacts


def get_city_options(contacts):
    cities = []

    for contact in contacts:
        city = contact.get("city", "")

        if city:
            cities.append(city)

    unique_cities = sorted(set(cities))

    return ["Усі міста"] + unique_cities


def filter_contacts(contacts, search_text, selected_city):
    result = []

    clean_search = search_text.strip().lower()

    for contact in contacts:
        clean_name = contact.get('name', '').strip().lower()
        clean_email = contact.get('email', '').strip().lower()
        clean_phone = contact.get('phone', '').strip().lower()

        # 1. чи є текст в name, email, phone
        matches_search = (clean_search in clean_name
                          or clean_search in clean_email
                          or clean_search in clean_phone
                          or not clean_search)

        # 2. чи підходить місто
        matches_city = (contact.get('city', '') == selected_city
                        or selected_city == 'Усі міста')

        if matches_search and matches_city:
            result.append(contact)

    return result


def show_contacts_page():
    st.set_page_config(
        page_title="Мої Контакти", page_icon="👥️"
    )

    st.title('Список контактів')

    contacts = load_contacts()

    list_tab, add_tab, del_tab = st.tabs(["Мої Контакти", "Додати Контакт", "Видалити Контакт"])

    with add_tab:
        is_success, error_message, contact = get_contact_form_data(contacts)

        if is_success:
            contacts.append(contact)
            save_contacts(contacts)
            st.success("Контакт збережено.")
        elif error_message:
            st.error(error_message)

    with list_tab:
        st.subheader("Список контактів")
        if contacts:
            search_text = st.text_input("Пошук")
            selected_city = st.selectbox("Місто:", get_city_options(contacts))
            filtered_contacts = filter_contacts(contacts, search_text, selected_city)

            st.write(f"Усього контактів: {len(contacts)}")
            st.write(f"Знайдено контактів: {len(filtered_contacts)}")

            display_contacts_tabular(filtered_contacts)
        else:
            st.info("Поки що контактів немає.")

    with del_tab:
        st.subheader("Видалення контакту")

        if contacts:
            contact = st.selectbox(
                "Контакти",
                contacts,
                format_func=lambda contact: str(contact["id"]) + " - " + contact["name"]
            )

            if st.button("Видалити"):
                contacts = delete_contact_by_id(contacts, contact["id"])
                save_contacts(contacts)
                st.success("Контакт видалено")
                time.sleep(3)
                st.rerun()
        else:
            st.info("Поки що немає контактів для видалення.")
