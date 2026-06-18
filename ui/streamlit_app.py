"""FinCopilot — self-contained Streamlit app.

Calls the agent DIRECTLY (no separate FastAPI backend), so it runs on Streamlit
Community Cloud. Reads the Gemini key from Streamlit Secrets (cloud) or the
local .env, and builds the vector index on first run if it's missing.

Run locally:   streamlit run ui/streamlit_app.py
"""

import os
import sys
from pathlib import Path

import streamlit as st

# Make the project root importable (Streamlit runs this file directly).
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

st.set_page_config(page_title="FinCopilot", page_icon="📋")

# Provide the API key from Streamlit Secrets (cloud) BEFORE importing app code.
# Locally there's no secrets file, so the .env is used instead.
try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass


def _password_ok() -> bool:
    """Optional gate: set APP_PASSWORD in Secrets to require a password."""
    try:
        expected = st.secrets.get("APP_PASSWORD")
    except Exception:
        expected = None
    if not expected:
        return True
    if st.session_state.get("authed"):
        return True
    pw = st.text_input("Access password", type="password")
    if pw and pw == expected:
        st.session_state["authed"] = True
        return True
    if pw:
        st.error("Wrong password.")
    return False


if not _password_ok():
    st.stop()


@st.cache_resource(show_spinner="Preparing knowledge base (first load only)…")
def _load_agent():
    """Build the index if needed and return the agent. Runs once per session."""
    from app.ingest.embed_store import ensure_index
    from app.graph.agent import run_agent

    ensure_index()
    return run_agent


run_agent = _load_agent()

st.title("📋 FinCopilot")
st.caption("Financial compliance & research copilot — cited answers over RBI regulation.")

if "history" not in st.session_state:
    st.session_state.history = []

for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.markdown(turn["content"])

question = st.chat_input("Ask a compliance question…")
if question:
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.history.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("Searching RBI regulation…"):
            try:
                result = run_agent(question)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        st.markdown(result["answer"])

        cites = [] if result.get("refused") else result.get("citations", [])
        if cites:
            with st.expander("Sources"):
                for src in cites:
                    st.markdown(f"- {src}")

        sources = "\n".join(f"- {s}" for s in cites)
        saved = result["answer"] + (f"\n\n**Sources:**\n{sources}" if sources else "")
        st.session_state.history.append({"role": "assistant", "content": saved})
