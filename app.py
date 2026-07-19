import streamlit as st

from contacts_app.app import show_contacts_page
from about_page import show_about_page


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
