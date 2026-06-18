# FinCopilot — Planning

Working name for a from-scratch **financial compliance & research copilot**:
ask a question → get a **cited**, evidence-grounded answer over a regulatory +
private-document corpus → an automated **compliance guardrail** reviews every
answer before it's shown.

## Documents
1. [What & Why](00-what-why.md) — the problem, the product, the 7-tech stack, non-goals.
2. [Goals](01-goals.md) — success criteria + the metrics we track.
3. [Timeline](02-timeline.md) — ~10-week plan to a demoable prototype.

## The stack (why each exists)
LLM Gateway · LangChain · LangGraph · RAG · Vectorless RAG · Guardrails · LLM Evaluation
— see [What & Why §4](00-what-why.md#4-why-this-technology-stack-the-7-pieces-mapped).

## Status
- [x] Planning docs
- [x] Corpus decided → **public RBI Digital Lending + KYC regulation** (no private data needed)
- [ ] Week 0–1: project scaffold + download corpus + write eval Q&A
- [ ] Week 2–3: thin vertical slice (first cited answer)

## Corpus (decided)
Public, downloadable Indian regulation — **scope: Digital Lending + KYC/AML**.
Zero data dependency; build starts immediately. The fintech contact is a
**pilot/validation partner**, not a build blocker.
