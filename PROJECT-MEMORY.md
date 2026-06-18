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
Answer-generation LLM = **Google Gemini (free tier)**, called via **litellm** (the
gateway pillar), model string `gemini/gemini-1.5-flash`, key in `.env` as
`GEMINI_API_KEY`. Embeddings stay local. Get a free key at aistudio.google.com.

## Status (2026-06-12)
Week 0–1 scaffold complete. **Next:** download 5 public RBI PDFs into
`data/corpus/`, write ~20 eval questions in `eval/questions.yaml`, then Week 2–3
thin RAG slice (question → cited answer).
