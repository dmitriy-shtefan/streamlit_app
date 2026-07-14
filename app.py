import os
import streamlit as st
from crewai import Agent, Crew, Task, LLM, Process

# streamlit run app.py
# OPENROUTER_API_KEY = "fksdhafkljshfjkhdfjahsj"


OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1'
DEFAULT_MODEL = 'openai/gpt-4o-mini'


def get_api_key():
    try:
        return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        return os.getenv("OPENROUTER_API_KEY") or ""


def create_llm(api_key, model, temperature):
    return LLM(
        model=model,
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        temperature=temperature,
        timeout=120
    )


def create_agent(role, goal, backstory, llm):
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm=llm,
        verbose=True,
        allow_delegation=False
    )


def build_crew(topic, llm):
    strategist = create_agent(
        role='Marketing Strategist',
        goal='Сформувати чітку концепцію маркетингової кампанії для бізнес-задачі.',
        backstory=(
            'Ви стратег з маркетингу, який швидко перетворює опис продукту або бізнес-цілі '
            'на зрозуміле позиціонування, аудиторії та ключові повідомлення.'
        ),
        llm=llm
    )

    channel_planner = create_agent(
        role='Channel Planner',
        goal='Підібрати ефективні канали кампанії і пояснити роль кожного з них.',
        backstory=(
            'Ви performance-маркетолог. Ви думаєте про шлях клієнта, бюджет, '
            'канали комунікації, формат контенту і прості метрики успіху.'
        ),
        llm=llm
    )

    copywriter = create_agent(
        role='Campaign Copywriter',
        goal='Створити тексти кампанії для різних каналів у єдиному тоні.',
        backstory=(
            'Ви копірайтер, який пише коротко, конкретно і під бізнес-результат. '
            'Ви адаптуєте одне повідомлення для email, соцмереж, реклами і сайту.'
        ),
        llm=llm
    )

    reviewer = create_agent(
        role='Brand and Risk Reviewer',
        goal='Перевірити кампанію на узгодженість, ризики і практичність запуску.',
        backstory=(
            'Ви маркетинговий reviewer. Ви помічаєте нечіткі обіцянки, слабкі CTA, '
            'ризики для бренду, юридичні нюанси і місця, де буде складно виміряти ефективність кампанії.'
        ),
        llm=llm
    )

    strategy_task = Task(
        description=(
            f'Тема: {topic} + Підготуйте основу маркетингової кампанії: '
            f'бізнес-мету, цільову аудиторію, головний інсайт, позиціонування і ключову пропозицію.'
        ),
        expected_output=(
            'Markdown-секція українською з пунктами: Мета, Аудиторія, Інсайт, Позиціонування, '
            'Ключова пропозиція.'
        ),
        agent=strategist
    )

    channels_task = Task(
        description=(
            f'Тема: {topic} + На основі стратегії запропонуйте план каналів кампанії: які канали використати, '
            f'яку роль має кожен канал, які формати контенту потрібні і які метрики варто відстежувати.'
        ),
        expected_output=(
            'Markdown-таблиця: Канал | Роль у кампанії | Формат | Метрика успіху.'
        ),
        agent=channel_planner,
        context=[strategy_task]
    )

    copy_task = Task(
        description=(
            f'Створіть набір коротких текстів для кампанії на основі стратегії і плану каналів:'
            f' headline, рекламний текст,'
            f' пост для соцмереж, email subject, короткий CTA.'
        ),
        expected_output=(
            'Markdown-секція з готовими текстами: Headline, Ad copy, Social post, Email subject, CTA.'
        ),
        agent=copywriter,
        context=[strategy_task, channels_task]
    )

    review_task = Task(
        description=(
            f'Перевірте кампанію перед запуском. Назвіть слабкі місця, ризики для бренду або довіри, '
            f'нечіткі обіцянки, проблеми з вимірюванням і запропонуйте конкретні покращення.'
        ),
        expected_output=(
            'Markdown-таблиця: Ризик або слабке місце | Як покращити.'
        ),
        agent=reviewer,
        context=[strategy_task, channels_task, copy_task]
    )

    final_task = Task(
        description=(
            'Зберіть фінальний план маркетингової кампанії на основі попередніх результатів. Пишіть коротко, '
            'структуровано і практично, щоб це можна було використати як основу для реального запуску.'
        ),
        expected_output=(
            'Markdown з секціями: Назва кампанії, Бізнес-мета, Цільова аудиторія, Ключове повідомлення, '
            'Канали, Готові тексти, Метрики, Ризики.'
        ),
        agent=strategist,
        context=[strategy_task, channels_task, copy_task, review_task]
    )

    return Crew(
        agents=[strategist, channel_planner, copywriter, reviewer],
        tasks=[strategy_task, channels_task, copy_task, review_task, final_task],
        process=Process.sequential,
        verbose=True
    )







st.title('CrewAI Marketing Campaign Demo')
st.caption('Multi-agent workflow: Strategy -> Channels -> Copy -> Review -> Campaign Brief.')


with st.sidebar:
    model = st.selectbox('Модель', [DEFAULT_MODEL])
    temperature = st.slider('Температура: ', 0.0, 1.2, 0.7, 0.1)


api_key = get_api_key()
if not api_key:
    st.warning('Додайте OPENROUTER_API_KEY ключ у Streamlit secrets')

topic = st.text_area('Продукт, послуга або бізнес-задача для кампанії.',
                     value='Підготовка маркетингової кампанії нового Python курсу',
                     height=90)


if st.button('Запустити CrewAI-команду', type="primary"):
    if not api_key:
        st.stop()

    with st.spinner('CrewAI запускає агентів..'):
        llm = create_llm(api_key, model, temperature)
        crew = build_crew(topic, llm)
        result = crew.kickoff()

    st.session_state.crewai_result = str(result)

if 'crewai_result' in st.session_state:
    st.header('Фінальний результат CrewAI')
    st.markdown(st.session_state.crewai_result)
    st.download_button(
        'Завантажити результат CrewAI',
        st.session_state.crewai_result,
        file_name='marketing_campaing.md',
        mime='text/markdown'
    )

