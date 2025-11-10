"""Streamlit entrypoint for Streamlit Community Cloud.

This file intentionally imports `JqlBuilder` which contains the Streamlit
application at top-level. Streamlit runs the top-level code, so importing the
module displays the app.

When deploying to Streamlit Community Cloud, the platform will execute this
file automatically if it's named `streamlit_app.py`.
"""

try:
    import JqlBuilder  # noqa: F401 - module side-effects create the app UI
except Exception as exc:  # pragma: no cover - fatal at runtime
    # If import fails (for example missing dependencies), surface a clear
    # message so the platform logs show the cause.
    print("Failed to import JqlBuilder:", exc)
    raise
