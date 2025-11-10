import streamlit as st
import pandas as pd

# Import helpers with a local-first import and a package fallback so the file
# is runnable both as a module and as a standalone Streamlit script.
try:
    from jira_utils import (
        connect_jira,
        get_project_options,
        get_project_components,
        get_issue_types as get_issue_types_from_jira,
        get_statuses as get_statuses_from_jira,
        run_jql,
    )
    from jql_utils import build_jql
except Exception:
    from stats.JqlSearch.jira_utils import (
        connect_jira,
        get_project_options,
        get_project_components,
        get_issue_types as get_issue_types_from_jira,
        get_statuses as get_statuses_from_jira,
        run_jql,
    )
    from stats.JqlSearch.jql_utils import build_jql
from datetime import datetime, time as dt_time


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
        jira = connect_jira(jira_url, jira_email, jira_token)
        st.success("Connected to Jira")
        st.session_state["jira"] = jira
    except Exception as exc:
        st.error(f"Failed to connect: {exc}")

if "jira" in st.session_state:
    jira = st.session_state["jira"]

    with st.spinner("Loading metadata..."):
        project_options = get_project_options(jira)

    # st.subheader("Build Query")

    project = st.selectbox("Select Project", options=list(project_options.keys()))

    components = get_project_components(jira, project)
    issue_types = get_issue_types_from_jira(jira)
    statuses = get_statuses_from_jira(jira)

    col1, col2, col3 = st.columns(3)

    issue_type = col1.multiselect("Issue Type", options=issue_types)
    status = col2.multiselect("Status", options=statuses)
    component = col3.multiselect("Component", options=components)

    # Advanced options
    with st.expander("Advanced JQL features", expanded=False):
        summary_contains = st.text_input("Summary contains (text search)")
        def _pick_datetime(label, key):
            enabled = st.checkbox(f"{label}", key=f"{key}_enable")
            if not enabled:
                return ""
            date_val = st.date_input(f"{label} (date)", key=f"{key}_date")
            time_val = st.time_input(f"{label} (time)", value=dt_time(0, 0), key=f"{key}_time", step=60)
            return datetime.combine(date_val, time_val).strftime("%Y-%m-%d %H:%M")

        created_after = _pick_datetime("Created after", "created_after")
        created_before = _pick_datetime("Created before", "created_before")
        updated_after = _pick_datetime("Updated after", "updated_after")
        updated_before = _pick_datetime("Updated before", "updated_before")
        attachments_opt = st.selectbox("Attachments", ["", "Has attachments", "No attachments"]) 
        labels_txt = st.text_input("Labels (comma separated)")

    # ORDER BY toggle (single-field)
    if "order_by" not in st.session_state:
        st.session_state["order_by"] = {"active": False, "field": None, "dir": "ASC"}

    with st.expander("ORDER BY / Sorting", expanded=False):
        order_active = st.checkbox("Enable ORDER BY", value=st.session_state["order_by"]["active"]) 
        st.session_state["order_by"]["active"] = order_active
        if order_active:
            fields = ["created", "updated", "priority", "assignee", "status", "issuetype", "key"]
            field = st.selectbox("Field", options=fields, index=0 if st.session_state["order_by"]["field"] not in fields else fields.index(st.session_state["order_by"]["field"]))
            direction = st.selectbox("Direction", options=["ASC", "DESC"], index=0 if st.session_state["order_by"]["dir"] == "ASC" else 1)
            st.session_state["order_by"]["field"] = field
            st.session_state["order_by"]["dir"] = direction

    advanced = {
        "summary_contains": summary_contains,
        "created_after": created_after,
        "created_before": created_before,
        "updated_after": updated_after,
        "updated_before": updated_before,
        "attachments_opt": attachments_opt,
        "labels_txt": labels_txt,
    }

    jql = build_jql(
        project=project,
        issue_type=issue_type,
        status=status,
        component=component,
        advanced=advanced,
        order_by=st.session_state["order_by"],
    )

    st.text_area("JQL Preview", jql, height=120, disabled=True)

    run = st.button("Run Query")

    if run:
        with st.spinner("Executing query..."):
            result = run_jql(jira, jql, max_results=200)

        if "issues" in result:
            rows = []
            for issue in result["issues"]:
                fields = issue["fields"]
                created_raw = fields.get("created", "")
                try:
                    created = pd.to_datetime(created_raw).strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    created = created_raw

                rows.append({
                    "Key": issue["key"],
                    "Summary": fields.get("summary", ""),
                    "Status": fields.get("status", {}).get("name", ""),
                    "Assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else "Unassigned",
                    "Created": created,
                })

            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)
            st.download_button("Export to CSV", data=df.to_csv(index=False), file_name="jira_results.csv")
        else:
            st.warning("No results found.")
