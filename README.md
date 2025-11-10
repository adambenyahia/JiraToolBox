# Jira JQL Builder — Streamlit deployment

This repository contains a Streamlit-based UI to build and run Jira JQL
queries. The primary app code is in `JqlBuilder.py`.

How to run locally

1. Create a virtual environment and activate it (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run streamlit_app.py
```

or directly:

```bash
streamlit run JqlBuilder.py
```

Deploying to Streamlit Community Cloud

- Ensure this repository is pushed to GitHub.
- In Streamlit Community Cloud, create a new app and point it to this
  repository. Set the app entry file to `streamlit_app.py` (the platform also
  recognizes `app.py`/`main.py` or you can point directly to
  `JqlBuilder.py`).
- Streamlit Cloud will install the packages from `requirements.txt`.

Notes

- The app requires Jira credentials (URL, email, API token) to connect.
- The code uses `atlassian-python-api` (imported as `atlassian` in the code).
- If you change dependencies, update `requirements.txt` accordingly.
