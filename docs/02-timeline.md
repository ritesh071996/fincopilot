# FinCopilot — Timeline

> ~10-week plan to a demoable prototype, building from scratch, solo.
> Principle: **ship a thin end-to-end slice early (Week 3), then deepen.**
> Don't build all 7 technologies before anything works — get one question
> answered with a citation first, then layer quality on top.

---

## At a glance

| Phase | Weeks | Outcome |
|---|---|---|
| 0 — Setup & scope | 1 | Repo, environment, corpus decided with contact |
| 1 — Thin vertical slice | 2–3 | One question → cited answer, end-to-end |
| 2 — Orchestration & guardrails | 4–5 | LangGraph agent + compliance guardrail |
| 3 — Vectorless RAG + Gateway | 6–7 | Second retrieval path; model routing & cost |
| 4 — Evaluation & hardening | 8–9 | Eval harness, hit the metric targets |
| 5 — Demo polish | 10 | Clean UI + demo script for the contact |

---

## Week 0–1 — Setup & scope
- [ ] Project scaffold: Python + FastAPI backend, repo, virtualenv, secrets handling.
- [ ] Pick the **stack defaults**: vector store (start simple — Chroma/pgvector), a minimal chat UI (Streamlit for speed), LangChain/LangGraph installed.
- [ ] **Download the public corpus:** RBI Digital Lending Guidelines + KYC Master Direction + related circulars (no contact needed — all public).
- [ ] Write **20 real Q&A pairs** from those documents → seeds the eval set.
- **Milestone:** environment runs; public corpus + question list exist.

## Week 2–3 — Thin vertical slice (the most important milestone)
- [ ] Ingest pipeline: load docs → chunk → embed → store.
- [ ] Basic **RAG**: retrieve top-k chunks → single LLM call → answer **with inline citations**.
- [ ] Minimal chat UI wired to the backend.
- **Milestone:** you can ask a real question and get a cited answer end-to-end. **Show the contact.**

## Week 4–5 — Orchestration & guardrails
- [ ] Replace the single call with a **LangGraph** graph: retrieve → draft → review → (amend) → answer, with loop caps.
- [ ] **Input guardrail:** scope check, PII detection, prompt-injection check.
- [ ] **Output guardrail:** citations-required, no-invented-numbers, compliance scoring + amend loop.
- **Milestone:** unsafe/uncited answers get blocked or fixed automatically.

## Week 6–7 — Vectorless RAG + LLM Gateway
- [ ] Build the **Vectorless RAG** path (document-tree navigation) for structured docs.
- [ ] A/B it against vector RAG on the eval set — keep the winner per document type.
- [ ] Put an **LLM Gateway** (e.g. LiteLLM) in front: route a cheap model for extraction + a strong model for synthesis, add fallback + cost tracking.
- **Milestone:** two retrieval strategies compared with data; all model calls routed + costed.

## Week 8–9 — Evaluation & hardening
- [ ] Build the **eval harness**: run the labeled set, LLM-as-judge, report accuracy / citation coverage / refusal correctness.
- [ ] Iterate prompts/retrieval until the **Goals metrics** are hit (≥80% accuracy, ≥95% citation coverage, 0 hallucinated numbers).
- [ ] Add the **audit log** (retrieved sources + scores per answer).
- **Milestone:** metrics dashboard green; every answer is auditable.

## Week 10 — Demo polish
- [ ] Tighten the UI (citations clickable, refusals clear, sources visible).
- [ ] Write a **demo script**: 10 questions that show grounding, refusal, and audit trail.
- [ ] Dry-run, then present to the contact as a pilot proposal.
- **Milestone:** a confident, repeatable demo + a pilot ask.

---

## Reality checks
- **No critical-path data dependency** — the corpus is public, so Week 0–1 can start today. (The contact is a Phase-2 pilot partner, not a blocker.)
- **Timeline assumes part-time solo + learning.** Full-time → compress ~30%. New to LangGraph → Week 4–5 may stretch; that's fine.
- **If forced to cut:** keep RAG + guardrails + eval. Vectorless RAG and the gateway are the safest things to defer to Phase 2.
- **Don't gold-plate the UI.** The product is the grounded answer, not the chrome.
