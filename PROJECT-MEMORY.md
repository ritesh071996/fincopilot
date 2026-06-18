# FinCopilot — Project Memory

Persistent context for this project. (Working name: FinCopilot.)

## What this is
A from-scratch fintech project — a document-grounded financial **compliance &
research copilot**. Ask a question → cited answer over a public RBI corpus → a
compliance guardrail reviews every answer before display.
**MVP scope: Digital Lending + KYC/AML.**

> Separate product from the medical "Sentinel"/lattice codebase at `C:\SENTINEL`
> — do **not** reuse that code; this is built fresh.

## Why these choices
- First project of this kind for the owner; learning the stack is an explicit goal.
- Warm **fintech contact** exists → a pilot/validation partner, **not** a blocker.
- **No private data** → corpus is **public RBI regulation** (zero data dependency).
- **India-first.**

## Stack (the 7 chosen technologies)
LLM Gateway (LiteLLM) · LangChain · LangGraph · RAG (Chroma) · Vectorless RAG ·
Guardrails · LLM Evaluation. Backend: FastAPI. UI: Streamlit.

## Setup facts
- Location: `C:\fincopilot`
- Python **3.13.2** (owner's installed version); venv at `C:\fincopilot\.venv`
- Dependencies installed; app boots (`uvicorn app.main:app --reload` → `/health` OK)
- Most modules are documented stubs raising `NotImplementedError`, filled in per
  the timeline. Planning docs in `docs/` (what-why, goals, timeline, corpus-checklist).
- Models default to OpenAI `gpt-4o-mini` via the gateway — **not locked**;
  revisit and verify current model/pricing when wiring real model calls.

## Working style (IMPORTANT)
From 2026-06-12: the **owner writes all code manually**. Claude's role is to
**guide** — explain what to build, why, where, and how to verify — in small
steps, and review/debug. Do **not** write code or run commands for them unless
asked. Wait for the explicit signal **"Lets go"** before acting on each step.

## Gotcha: PyTorch + SSL segfault on this Windows machine (SOLVED)
Any SSL/HTTPS call made AFTER torch is imported segfaults (exit -1073741819 /
0xC0000005) — a torch-on-Windows OpenSSL DLL clash. **Root fix:** initialize SSL
BEFORE torch loads — `import ssl; ssl.create_default_context()` at the top of
`app/__init__.py` (runs before any submodule imports torch). Verified: HTTPS after
torch then works. This makes runtime LLM API calls (Gemini) safe even though
embeddings load torch first.
Also for HF model downloads: pre-download via `huggingface_hub` in a process
WITHOUT torch, then load offline with `HF_HUB_OFFLINE=1` / `TRANSFORMERS_OFFLINE=1`
(set in `app/config.py`). Embedding model `all-MiniLM-L6-v2` (384-dim) is cached
under `C:\Users\LENOVO\.cache\huggingface`.

## LLM backend choice (2026-06-12)
**Demo runs on Gemini free tier**, model `gemini/gemini-2.5-flash-lite` (its own
daily quota bucket + higher limit + faster than 2.5-flash, which is capped at
only 20 req/DAY and gets exhausted fast by the multi-call agent). Key in `.env`
as `GEMINI_API_KEY`. **OpenAI key was REMOVED** at user's request (cost concern;
demo-only use). For heavier/eval use, OpenAI gpt-4o-mini is more reliable but
costs (user declined). Gateway retries transient errors (429/503). Embeddings
local. NOTE: free tier still limited — pace demo questions; ~2-4 calls each.

## Status (2026-06-12) — WORKING PROTOTYPE (paused here by choice)
Full end-to-end compliance copilot works in the Streamlit UI. Eval scorecard:
100% accuracy / citations / refusal (14 answerable + 4 refuse). Committed at
git `8a31528`.

**Done — 5 of the 7 technologies:** LangChain, LangGraph (agent: retrieve→draft→
review→amend), RAG (Chroma, local embeddings), LLM Evaluation (harness+scorecard),
LLM Gateway (litellm→OpenAI gpt-4o-mini, retries). Guardrails = half (output
guardrail done; input guardrail not built). **Vectorless RAG = deliberately
dropped** (not needed; vector RAG works).

**Optional remaining (user said "enough" for now):** (1) retrieval recall fix —
known weakness: DLG-cap answer depends on question phrasing (top_k 5→8-10 or a
stronger embedding model); (2) input guardrail 8c (scope/injection); (3) polish:
clickable citations, harder eval questions.

**Run it:** two terminals from `C:\fincopilot` (venv active) — backend
`uvicorn app.main:app`, UI `streamlit run ui/streamlit_app.py`. Needs
OPENAI_API_KEY in `.env`. `scratch_embed_test.py` is a throwaway, safe to delete.
