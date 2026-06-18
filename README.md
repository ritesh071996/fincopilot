# FinCopilot
https://fincopilotgit-gyyhbhj6a2qgusyzh5qdop.streamlit.app/

A document-grounded **financial compliance & research copilot**. Ask a question
about Indian financial regulation → get a **cited**, evidence-grounded answer
over a public RBI corpus → an automated **compliance guardrail** reviews every
answer before it's shown.

> Working name. Status: prototype, Week 0–1 (scaffold). Built solo from scratch.
> Planning docs live in [`docs/`](docs/README.md).

## The stack (and why each exists)
LLM Gateway · LangChain · LangGraph · RAG · Vectorless RAG · Guardrails · LLM Evaluation
— see [docs/00-what-why.md §4](docs/00-what-why.md).

## Project layout
```
app/
  config.py        settings (reads .env)
  main.py          FastAPI entry point
  gateway/         LLM Gateway — all model calls route through here
  ingest/          load -> chunk -> embed -> store the RBI corpus
  rag/             retrieval (vector RAG now; vectorless RAG later)
  graph/           LangGraph agent: retrieve -> draft -> guardrail -> amend
  guardrails/      input + output safety / compliance checks
  api/             FastAPI routes
ui/                Streamlit chat UI
eval/              evaluation harness + question set
data/              corpus (RBI PDFs) + vector index   (gitignored)
docs/              planning: what/why, goals, timeline, corpus checklist
```

## Setup (Windows, Python 3.13)
```powershell
# 1. Create + activate a virtual environment
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure secrets
copy .env.example .env      # then edit .env and add your API key

# 4. Run the backend
uvicorn app.main:app --reload
#    -> http://127.0.0.1:8000/docs   (health check: /health)

# 5. (optional) Run the chat UI in a second terminal
streamlit run ui/streamlit_app.py
```

## Where things stand
Most modules are **documented stubs** that raise `NotImplementedError` — the
skeleton is in place; each piece is filled in on the schedule in
[docs/02-timeline.md](docs/02-timeline.md). The first working slice
(question → cited answer) lands in **Week 2–3**.

## Corpus
Public RBI regulation — **scope: Digital Lending + KYC/AML**. See
[docs/03-corpus-checklist.md](docs/03-corpus-checklist.md) for what to download
and where it goes.
