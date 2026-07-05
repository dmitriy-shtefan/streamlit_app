import streamlit as st


STUDENT = {
    "name": "Ім'я Студента",
    "role": "Python / Streamlit beginner developer",
    "location": "Україна",
    "email": "student@example.com",
    "github": "https://github.com/student",
    "about": (
        "Я вивчаю Python і створюю прості web-застосунки, які вирішують "
        "практичні задачі: облік даних, фільтрація, збереження у файли "
        "та зрозумілий інтерфейс для користувача."
    ),
}

SKILLS = [
    {"name": "Python basics", "level": 85},
    {"name": "Functions", "level": 75},
    {"name": "Lists and dictionaries", "level": 80},
    {"name": "JSON / CSV files", "level": 70},
    {"name": "Streamlit UI", "level": 75},
    {"name": "Git and GitHub", "level": 55},
]

COURSE_TOPICS = [
    "змінні, типи даних і розрахунки",
    "умови, логічні оператори і валідація",
    "цикли for та while",
    "списки, словники, множини і кортежі",
    "функції і структура програми",
    "читання та запис файлів",
    "Streamlit, форми, таблиці і фільтри",
]


def make_resume_markdown():
    skills = ", ".join(skill["name"] for skill in SKILLS)
    topics = "\n".join(f"- {topic}" for topic in COURSE_TOPICS)

    return f"""# {STUDENT["name"]}

**Role:** {STUDENT["role"]}
**Location:** {STUDENT["location"]}
**Email:** {STUDENT["email"]}
**GitHub:** {STUDENT["github"]}

## About me

{STUDENT["about"]}

## Skills

{skills}

## Course topics

{topics}

## Portfolio projects

Personal Budget Tracker - Streamlit-застосунок для обліку доходів і витрат.

Список контактів - Streamlit-застосунок для збереження контактів у JSON,
пошуку, фільтрації, видалення та експорту у CSV.
"""


def show_resume_page():
    st.title("Інтерактивне резюме")

    left, right = st.columns([2, 1])

    with left:
        st.header(STUDENT["name"])
        st.subheader(STUDENT["role"])
        st.write(STUDENT["about"])

    with right:
        st.metric("Проєктів у портфоліо", 2)
        st.metric("Технологій", len(SKILLS))
        st.metric("Формат", "Streamlit")

    st.divider()

    st.subheader("Навички")
    for skill in SKILLS:
        st.write(skill["name"])
        st.progress(skill["level"] / 100)

    st.subheader("Що вивчено на курсі")
    for topic in COURSE_TOPICS:
        st.write("- " + topic)

    st.subheader("Портфоліо-проєкт")
    with st.container(border=True):
        st.markdown("### Personal Budget Tracker")
        st.write(
            "Застосунок для обліку особистих доходів і витрат. "
            "Користувач може додавати записи, фільтрувати їх, бачити баланс "
            "і аналізувати витрати за категоріями."
        )
        st.write("Технології: Python, Streamlit, JSON, списки, словники, функції.")

    with st.container(border=True):
        st.markdown("### Список контактів")
        st.write(
            "Застосунок для збереження контактів. Користувач може додавати, "
            "видаляти, шукати і фільтрувати контакти, а також експортувати "
            "дані через CSV."
        )
        st.write("Технології: Python, Streamlit, JSON, CSV, форми, таблиці, фільтри.")

    st.subheader("Контакти")
    contact_left, contact_right = st.columns(2)
    contact_left.write(f"Email: {STUDENT['email']}")
    contact_right.write(f"GitHub: {STUDENT['github']}")

    st.download_button(
        "Завантажити резюме як Markdown",
        make_resume_markdown(),
        file_name="student_resume.md",
        mime="text/markdown",
    )
