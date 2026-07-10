import os

import requests
import streamlit as st
from openrouter import ask_openrouter

DEFAULT_MODEL = "tencent/hy3:free"

def get_api_key():
    try:
        return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        return os.getenv("OPENROUTER_API_KEY") or ""


st.title("AI-команда за 5 хвилин")
st.caption("Streamlit керує кількома AI-ролями через OpenRouter REST API.")

with st.sidebar:
    model = st.text_input("OpenRouter model", DEFAULT_MODEL)
    temperature = st.slider("Temperature", 0.0, 1.2, 0.7, 0.1)

topic = st.text_area(
    "Ідея студента або тема демо",
    value="AI-асистент, який допомагає студенту спланувати Python-застосунок",
    height=90,
)

api_key = get_api_key()
if not api_key:
    st.warning("Додайте `OPENROUTER_API_KEY` у змінні середовища або Streamlit secrets.")

roles = {
    "Візіонер": "Ви придумуєте ефектну ідею демо і пояснюєте, чому вона виглядає цікаво для студентів.",
    "Інженер": "Ви перетворюєте ідею на простий технічний план Python-застосунку.",
    "Критик": "Ви шукаєте ризики, слабкі місця і способи зробити демо надійнішим.",
}

if "agent_answers" not in st.session_state:
    st.session_state.agent_answers = {}

run_demo = st.button("Запустити AI-команду", type="primary")

if run_demo:
    if not api_key:
        st.error("Не знайдено `OPENROUTER_API_KEY`.")
        st.stop()

    st.session_state.agent_answers = {}

    columns = st.columns(3)
    for column, (role_name, role_prompt) in zip(columns, roles.items()):
        with column:
            st.subheader(role_name)
            with st.spinner(f"{role_name} думає..."):
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "Відповідайте українською, коротко і конкретно. "
                            "Формат: 3-5 bullet points."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"{role_prompt}\n\nТема: {topic}",
                    },
                ]
                answer = ask_openrouter(
                    api_key=api_key,
                    messages=messages,
                    model=model,
                    temperature=temperature,
                )
            st.session_state.agent_answers[role_name] = answer
            st.markdown(answer)

if st.session_state.agent_answers:
    st.divider()
    st.header("Фінальний план від AI-директора")

    joined_answers = "\n\n".join(
        f"## {role}\n{answer}"
        for role, answer in st.session_state.agent_answers.items()
    )

    director_prompt = f"""
    Тема: {topic}

    Ось відповіді трьох AI-ролей:

    {joined_answers}

    Збери з них один короткий план демо для заняття:
    1. Що показати студентам.
    2. Як це працює технічно.
    3. Які Python/AI concepts пояснити після демо.
    4. Які ризики live demo врахувати.
    """

    if st.button("Зібрати фінальний план"):
        if not api_key:
            st.error("Не знайдено `OPENROUTER_API_KEY`.")
            st.stop()

        with st.spinner("AI-директор збирає результат..."):
            messages = [
                {
                    "role": "system",
                    "content": (
                        "Ви AI-директор навчального демо. "
                        "Пишіть українською, структуровано і практично."
                    ),
                },
                {"role": "user", "content": director_prompt},
            ]
            final_plan = ask_openrouter(
                api_key=api_key,
                messages=messages,
                model=model,
                temperature=0.4,
            )

        st.session_state.final_plan = final_plan

    if "final_plan" in st.session_state:
        st.markdown(st.session_state.final_plan)
        st.download_button(
            "Завантажити Markdown",
            st.session_state.final_plan,
            file_name="wow_streamlit_demo_plan.md",
            mime="text/markdown",
        )

