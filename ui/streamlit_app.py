"""Minimal chat UI. Calls the FastAPI backend's /api/v1/ask endpoint.

Run (with the backend already running on :8000):
    streamlit run ui/streamlit_app.py
"""

import httpx
import streamlit as st

API_URL = "http://127.0.0.1:8000/api/v1/ask"

st.set_page_config(page_title="FinCopilot", page_icon="📋")
st.title("📋 FinCopilot")
st.caption("Financial compliance & research copilot — cited answers over RBI regulation.")

# Keep the conversation across reruns.
if "history" not in st.session_state:
    st.session_state.history = []

# Replay past turns.
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
                resp = httpx.post(API_URL, json={"question": question}, timeout=120)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                st.error(f"Could not reach the backend at {API_URL}\n\n{e}")
                st.stop()

        st.markdown(data["answer"])

        if data.get("citations"):
            with st.expander("Sources"):
                for src in data["citations"]:
                    st.markdown(f"- {src}")

        # Save assistant turn (answer + sources) for replay.
        sources = "\n".join(f"- {s}" for s in data.get("citations", []))
        saved = data["answer"] + (f"\n\n**Sources:**\n{sources}" if sources else "")
        st.session_state.history.append({"role": "assistant", "content": saved})
