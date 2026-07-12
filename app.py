"""
Short WOW demo: Streamlit + CrewAI + OpenRouter.

Setup:
    pip install streamlit crewai
    export OPENROUTER_API_KEY="your_key"

Optional:
    export OPENROUTER_MODEL="openai/gpt-oss-120b:free"

Run:
    streamlit run wow_crewai_streamlit_demo.py
"""

import os

import streamlit as st
from crewai import Agent, Crew, LLM, Process, Task


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-oss-120b:free"

def get_api_key():
    try:
        return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        return os.getenv("OPENROUTER_API_KEY")


def create_llm(api_key, model, temperature):
    return LLM(
        model=model,
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        temperature=temperature,
        timeout=120,
    )


def create_agent(role, goal, backstory, llm):
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def build_crew(topic, llm):
    visionary = create_agent(
        role="AI Demo Visionary",
        goal="Придумати ефектну ідею демо, яка одразу зацікавить студентів.",
        backstory=(
            "Ви викладач-практик, який вміє перетворювати складні AI-теми "
            "на короткі й видовищні демонстрації."
        ),
        llm=llm,
    )

    engineer = create_agent(
        role="Python Engineer",
        goal="Перетворити ідею на простий технічний план Python-застосунку.",
        backstory=(
            "Ви Python-інженер, який цінує короткий код, зрозумілу структуру "
            "і демонстрації, які реально запускаються на занятті."
        ),
        llm=llm,
    )

    reviewer = create_agent(
        role="Live Demo Reviewer",
        goal="Знайти ризики live demo і запропонувати, як зробити показ надійнішим.",
        backstory=(
            "Ви критичний reviewer. Ви думаєте про API keys, rate limits, "
            "нестабільні відповіді моделей і час заняття."
        ),
        llm=llm,
    )

    editor = create_agent(
        role="Learning Experience Editor",
        goal="Зібрати відповіді агентів у короткий фінальний план для викладача.",
        backstory=(
            "Ви редактор навчальних матеріалів. Ваш результат має бути "
            "структурований, практичний і готовий для показу студентам."
        ),
        llm=llm,
    )

    idea_task = Task(
        description=(
            f"Тема: {topic}\n\n"
            "Запропонуйте вау-ідею демо для студентів Python. "
            "Поясніть, що саме вони побачать і чому це має виглядати цікаво."
        ),
        expected_output="3-5 bullet points українською і одна коротка назва демо.",
        agent=visionary,
    )

    engineering_task = Task(
        description=(
            f"Тема: {topic}\n\n"
            "На основі ідеї демо запропонуйте мінімальну технічну реалізацію: "
            "які файли, бібліотеки, змінні середовища і кроки запуску потрібні."
        ),
        expected_output="Markdown-секція з технічним планом і командами запуску.",
        agent=engineer,
        context=[idea_task],
    )

    review_task = Task(
        description=(
            "Перевірте демо як live-показ на занятті. Назвіть ризики і дайте "
            "короткі поради, як уникнути проблем під час демонстрації."
        ),
        expected_output="Markdown-таблиця: Ризик | Як зменшити.",
        agent=reviewer,
        context=[idea_task, engineering_task],
    )

    final_task = Task(
        description=(
            "Зберіть фінальний план демо для викладача на основі попередніх "
            "результатів. Пишіть коротко, структуровано і практично."
        ),
        expected_output=(
            "Markdown з секціями: Назва, Що показати студентам, Як це працює, "
            "Сценарій на 5 хвилин, Ризики live demo."
        ),
        agent=editor,
        context=[idea_task, engineering_task, review_task],
    )

    return Crew(
        agents=[visionary, engineer, reviewer, editor],
        tasks=[idea_task, engineering_task, review_task, final_task],
        process=Process.sequential,
        verbose=True,
    )


st.set_page_config(page_title="CrewAI WOW demo", page_icon="🤖", layout="wide")

st.title("CrewAI Demo")
st.caption("Multi-agent workflow: Agent -> Task -> Crew -> Result.")

with st.sidebar:
    model = st.text_input("OpenRouter model", os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL))
    temperature = st.slider("Temperature", 0.0, 1.2, 0.7, 0.1)

topic = st.text_area(
    "Ідея студента або тема демо",
    value="AI-команда, яка перетворює ідею студента на план Python-застосунку",
    height=90,
)

api_key = get_api_key()
if not api_key:
    st.warning("Додайте `OPENROUTER_API_KEY` у змінні середовища або Streamlit secrets.")

if st.button("Запустити CrewAI-команду", type="primary"):
    if not api_key:
        st.error("Не знайдено `OPENROUTER_API_KEY`.")
        st.stop()

    with st.spinner("CrewAI запускає агентів послідовно..."):
        llm = create_llm(api_key, model, temperature)
        crew = build_crew(topic, llm)
        result = crew.kickoff()

    st.session_state.crewai_result = str(result)

if "crewai_result" in st.session_state:
    st.header("Фінальний результат CrewAI")
    st.markdown(st.session_state.crewai_result)
    st.download_button(
        "Завантажити Markdown",
        st.session_state.crewai_result,
        file_name="crewai_wow_demo_plan.md",
        mime="text/markdown",
    )
