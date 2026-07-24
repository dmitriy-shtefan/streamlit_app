# Створіть функції `validate_email(email)` та `validate_phone(phone)`.
# Кожна з функцій повинна повертати кортеж з двох значень:
# - True або False
# - текст повідомлення


def validate_email(email):
    if "@" not in email:
        return False, "Email має містити @."

    if "." not in email:
        return False, "Email має містити крапку."

    return True, ""


def validate_phone(phone):
    if not phone:
        return False, "Телефон не має бути порожнім."

    if phone[0] != "+":
        return False, "Телефон має містити знак + на початку."

    digits = phone[1:]

    if not digits.isdigit():
        return False, "Телефон має містити лише цифри та знак + на початку."

    if len(digits) != 12:
        return False, "Телефон має містити 12 цифр."

    return True, ""
