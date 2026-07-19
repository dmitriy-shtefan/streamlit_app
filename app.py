from pathlib import Path
import sys

import streamlit as st

APP_DIR = Path(__file__).parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from contacts_page import show_contacts_page
from about_page import show_about_page


def main():
    st.set_page_config(
        page_title="Dmytro Shtefan",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    page = st.navigation(
        {
            "": [st.Page(show_about_page, title="Про мене", icon="👤", default=True)],
            "📁 Мої Проєкти": [st.Page(show_contacts_page, title="Список контактів", icon="👥")]
        },
        position="sidebar",
    )

    page.run()


if __name__ == "__main__":
    main()
