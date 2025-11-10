from typing import Iterable


def _format_list(values: Iterable[str]) -> str:
    return ", ".join([f'"{v}"' for v in values])


def in_or_eq(field: str, vals):
    """Return a JQL clause for a field and a value or list of values."""
    if not vals:
        return None
    if isinstance(vals, (list, tuple)):
        if len(vals) == 1:
            return f'{field} = "{vals[0]}"'
        return f"{field} IN ({_format_list(vals)})"
    return f'{field} = "{vals}"'


def build_jql(
    project: str,
    issue_type,
    status,
    component,
    advanced: dict,
    order_by: dict = None,
):
    """Build a JQL string from the provided pieces.

    advanced is a dict that may contain:
      - summary_contains
      - created_after / created_before
      - updated_after / updated_before
      - attachments_opt ("Has attachments" / "No attachments")
      - labels_txt (comma-separated string)
    order_by is a dict with keys: active(bool), field(str), dir(str)
    """
    conditions = [f'project = "{project}"']

    for field, vals in (("issuetype", issue_type), ("status", status), ("component", component)):
        clause = in_or_eq(field, vals)
        if clause:
            conditions.append(clause)

    if advanced.get("summary_contains"):
        conditions.append(f'summary ~ "{advanced["summary_contains"]}"')

    if advanced.get("created_after"):
        conditions.append(f'created >= "{advanced["created_after"]}"')
    if advanced.get("created_before"):
        conditions.append(f'created <= "{advanced["created_before"]}"')

    if advanced.get("updated_after"):
        conditions.append(f'updated >= "{advanced["updated_after"]}"')
    if advanced.get("updated_before"):
        conditions.append(f'updated <= "{advanced["updated_before"]}"')

    if advanced.get("attachments_opt") == "Has attachments":
        conditions.append("attachments IS NOT EMPTY")
    elif advanced.get("attachments_opt") == "No attachments":
        conditions.append("attachments IS EMPTY")

    labels_txt = (advanced.get("labels_txt") or "").strip()
    if labels_txt:
        labels = [item.strip() for item in labels_txt.split(",") if item.strip()]
        if len(labels) == 1:
            conditions.append(f'labels = "{labels[0]}"')
        else:
            conditions.append(f'labels IN ({_format_list(labels)})')

    jql = " AND ".join(conditions)

    if order_by and order_by.get("active") and order_by.get("field"):
        jql += f' ORDER BY {order_by["field"]} {order_by.get("dir", "ASC")}'

    return jql
