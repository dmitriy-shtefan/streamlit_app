from pathlib import Path
import sys

import streamlit as st


APP_DIR = Path(__file__).parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from budget_page import show_budget_page
from contacts_page import show_contacts_page
from resume_page import show_resume_page


def main():
    st.set_page_config(
        page_title="Student Portfolio Projects",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    with st.sidebar:
        st.title("Навігація")
        page = st.radio(
            "Сторінка",
            ["Резюме", "Personal Budget Tracker", "Список контактів"],
        )

        st.divider()
        st.caption("Фінальний проєкт курсу Python + Streamlit")

    if page == "Резюме":
        show_resume_page()
    elif page == "Personal Budget Tracker":
        show_budget_page()
    else:
        show_contacts_page()


if __name__ == "__main__":
    main()
