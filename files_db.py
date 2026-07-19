import json
import os

FILE_NAME = 'contacts.json'


# Функція save_contacts(contacts),
# яка зберігає список контактів у файл contacts.json
def save_contacts(contacts):
    with open(FILE_NAME, 'w', encoding='utf-8') as file:
        json.dump(contacts, file, ensure_ascii=False, indent=2)


# Функція load_contacts(),
# яка читає контакти з файлу contacts.json
def load_contacts():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, 'r', encoding='utf-8') as file:
        contacts = json.load(file)

    return contacts


# Функція make_contact_id(contacts),
# яка буде створювати новий унікальний ID для контакту
# [
#   {"id": 1, "name": "Oleg"},
#   {"id": 99, "name": "Olga"}
# ]
def make_contact_id(contacts):
    max_id = 0

    for contact in contacts:
        contact_id = contact.get("id", 0)

        if contact_id > max_id:
            max_id = contact_id

    return max_id + 1
