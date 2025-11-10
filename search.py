import streamlit as st
from atlassian import Jira
import pandas as pd

st.set_page_config(page_title="Jira Query Builder", layout="wide")

st.title("Jira Query Builder")

# Sidebar for credentials
st.sidebar.header("Jira Connection")

jira_url = st.sidebar.text_input("Jira URL", placeholder="https://your-domain.atlassian.net")
jira_email = st.sidebar.text_input("Email", placeholder="you@example.com")
jira_token = st.sidebar.text_input("API Token", type="password")

connect = st.sidebar.button("Connect")

if connect:
    try:
        jira = Jira(
            url=jira_url,
            username=jira_email,
            password=jira_token
        )

        st.success("Connected to Jira")
        st.session_state["jira"] = jira

    except Exception as e:
        st.error(f"Failed to connect: {e}")

if "jira" in st.session_state:

    jira = st.session_state["jira"]

    # Fetch metadata
    with st.spinner("Loading metadata..."):
        """
        This file was the original Streamlit search UI. The codebase was split into
        smaller modules and a new entrypoint called `JqlBuilder.py` was created.

        Run the app with:

            streamlit run stats/JqlSearch/JqlBuilder.py

        Or open `stats/JqlSearch/JqlBuilder.py` to view the refactored, modular code.
        """
    components = [c["name"] for c in components] if components else []
