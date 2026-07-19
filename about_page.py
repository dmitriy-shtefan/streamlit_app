from pathlib import Path

import streamlit as st

GITHUB_URL = "https://github.com/student"
EMAIL = "student@github.com"
AVATAR_PATH = Path(__file__).parent / "assets" / "profile-avatar.png"

def show_about_page():
    st.markdown(
        """
        <style>
            .hero-role {
                margin: 0 0 0.75rem;
                color: #2563eb;
                font-size: 1.1rem;
                font-weight: 600;
            }
            .profile-photo img {
                border-radius: 50%;
                border: 4px solid #dbeafe;
                box-shadow: 0 8px 20px rgba(37, 99, 235, 0.18);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    photo_column, intro_column = st.columns([1, 3], vertical_alignment="center")

    with photo_column:
        st.markdown("<div class='profile-photo'>", unsafe_allow_html=True)
        st.image(str(AVATAR_PATH), width=190)
        st.markdown("</div>", unsafe_allow_html=True)

    with intro_column:
        st.title("Дмитро")
        st.markdown("<p class='hero-role'>Junior Python Developer</p>", unsafe_allow_html=True)
        st.write("Створюю веб-застосунки на Python для автоматизації повсякденних задач.")

    st.subheader("Мої проєкти")

    with st.container(border=True):
        st.subheader("Список контактів")
        st.write(
            "Застосунок для збереження контактів. Користувач може додавати, "
            "видаляти, шукати і фільтрувати контакти."
        )
        st.write("Технології: Python, Streamlit, JSON, pandas.")

    st.subheader("Мої контакти")
    with st.container(border=True):
        st.write(f"Email: {EMAIL}")
        st.write(f"GitHub: {GITHUB_URL}")
