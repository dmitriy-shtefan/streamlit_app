import os
import streamlit as st

# streamlit run app.py
# OPENROUTER_API_KEY = "fksdhafkljshfjkhdfjahsj"

def get_api_key():
    try:
        return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        return os.getenv("OPENROUTER_API_KEY") or ""

