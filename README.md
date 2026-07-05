# Student Portfolio Projects

A Streamlit portfolio app with three student projects:

- interactive resume
- personal budget tracker with JSON storage, filters, charts, and CSV export
- contacts list with JSON storage, search, city filter, delete action, and CSV export

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy To Streamlit Cloud

1. Push this repository to GitHub.
2. Open Streamlit Cloud and create a new app from the repository.
3. Use `app.py` as the main file.
4. Deploy.

The app stores demo/user data in local JSON files. On Streamlit Cloud this storage is suitable for demos, but it is not durable database storage.
