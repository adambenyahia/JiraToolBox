from atlassian import Jira


def connect_jira(jira_url: str, jira_email: str, jira_token: str) -> Jira:
    """Return an authenticated Jira client."""
    return Jira(url=jira_url, username=jira_email, password=jira_token)


def get_project_options(jira: Jira):
    projects = jira.projects()
    return {p["key"]: p["name"] for p in projects}


def get_project_components(jira: Jira, project: str):
    comps = jira.get_project_components(project)
    return [c["name"] for c in comps] if comps else []


def get_issue_types(jira: Jira):
    types = jira.get_issue_types()
    return [t["name"] for t in types]


def get_statuses(jira: Jira):
    sts = jira.get_all_statuses()
    return [s["name"] for s in sts]


def run_jql(jira: Jira, jql: str, max_results: int = 200, fields=None):
    if fields is None:
        fields = ["summary", "status", "assignee", "created"]
    return jira.post(
        "/rest/api/3/search/jql",
        json={"jql": jql, "maxResults": max_results, "fields": fields},
    )
