# FinCopilot — Goals

> What "good" means, and how we'll know we got there. Measurable where possible.

---

## North Star
**A finance professional trusts FinCopilot's cited answer enough to act on it without re-reading the source documents themselves.**

If they still have to double-check everything by hand, we've failed — no matter how good the demo looks.

---

## Prototype success criteria (the bar for "done")
The prototype is successful when we can sit a real user (the contact's team) in front of it and:

1. They ask **10 real questions** from their actual work.
2. **≥ 8 / 10** answers are correct **and** every claim is backed by a correct citation.
3. On questions with **no supporting source**, it **refuses** instead of guessing (≥ 9/10 correct refusals).
4. They say some version of *"this would save me time."*

That's the whole game for the prototype. Everything below serves these four.

---

## Measurable goals (the metrics we track from day one)

| Metric | What it measures | Prototype target |
|---|---|---|
| **Answer accuracy** | Correct vs. our labeled eval set | ≥ 80% |
| **Citation coverage** | % of factual claims with a valid source | ≥ 95% |
| **Hallucinated numbers** | Answers stating a number not in any source | 0 (hard fail) |
| **Refusal correctness** | Correctly refuses when no source exists | ≥ 90% |
| **Guardrail catch rate** | Unsafe/uncited drafts blocked before display | ≥ 95% |
| **Latency (p50)** | Question → answer | ≤ 15s (prototype-acceptable) |
| **Cost / query** | Tracked via the LLM gateway | Known & logged (optimize later) |

> These aren't vanity metrics — accuracy + citation coverage + zero hallucinated numbers ARE the product.

---

## Learning goals (this is also a skill-build project)
By the end of the prototype, hands-on mastery of:
- **LangGraph** — building and debugging a stateful, multi-node agent.
- **RAG vs Vectorless RAG** — having built both and measured which wins on *your* documents.
- **Guardrails** — input + output validation that actually blocks bad output.
- **LLM Evaluation** — a real eval harness, not vibes.
- **LLM Gateway** — provider routing, fallback, and cost visibility.

---

## Phased goals (beyond the prototype)

**Phase 1 — Prototype (now → ~10 weeks):** one workflow, one corpus, demoable to the contact. *Goal: prove trust & usefulness.*

**Phase 2 — Pilot:** the contact's team uses it on real work for a few weeks; we measure time saved and tighten accuracy. *Goal: prove it survives real use.*

**Phase 3 — Product:** multi-user, access control, more document types, deployment. *Goal: something sellable.*

We do **not** build Phase 2/3 features during Phase 1. Scope discipline is a goal in itself.

---

## Non-goals for the prototype (deliberately deferred)
- Multi-tenant auth / user management — single workspace is fine.
- Fancy UI — a clean, minimal chat is enough.
- Scale / high availability — runs on one machine.
- Every document type — **one** corpus, **one** workflow, done well.
