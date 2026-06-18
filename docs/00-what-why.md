# FinCopilot — What & Why

> Working name. A document-grounded **financial compliance & research copilot**.
> Status: Prototype, building from scratch. Owner: Vansh.

---

## 1. One-line

FinCopilot answers regulated finance & compliance questions with **cited, evidence-grounded** answers drawn from a regulatory corpus + the user's own documents — and runs every answer through an **automated compliance guardrail** before a human ever sees it.

Think: *"Upload a circular, a policy, or a stack of financial documents → ask a question → get a citation-backed answer you can defend to an auditor."*

---

## 2. Why — the problem

Compliance, risk, and finance teams do enormous amounts of **reading and cross-referencing**:

- Regulations change constantly (RBI / SEBI circulars, tax rules, internal policy updates).
- Answers must be **traceable to a source** — "the model said so" is not acceptable to an auditor or a regulator.
- Generic LLMs (ChatGPT, etc.) are **banned or risky** in financial firms: they hallucinate numbers, cite nothing, and can leak confidential data to a third party.

So there's a painful gap: the people who most need a fast, grounded assistant are the ones who **can't safely use the generic tools**. That gap — *trust, grounding, and auditability* — is the product.

### Who it's for
- **Primary:** compliance / risk / operations teams at Indian fintechs (lenders, LSPs, NBFCs) who must stay compliant with RBI rules.
- **Secondary (later):** CAs, accounting firms, and SMBs with the same document-heavy pain.

### The corpus — decided (no private data needed)
The MVP is grounded entirely in **public, downloadable Indian regulation**, so we
have **zero data dependency** and can start immediately:

- RBI **Digital Lending Guidelines**
- RBI **KYC Master Direction**
- Related RBI circulars (outsourcing, fair practices, data localization)
- *(later)* SEBI and adjacent slices

**Scope = Digital Lending + KYC/AML compliance.** Bounded, current, heavily
enforced, and binding on every Indian fintech — so it demos to any contact.
The contact becomes a **pilot/validation partner**, not a build blocker; their
private documents plug in during the pilot, not the prototype.

---

## 3. What — what it does

```
User question
   │
   ▼
[ Guardrail: input check ]   ── scope? PII? prompt-injection? ──► refuse if unsafe
   │
   ▼
[ Retrieve ]   ── regulatory corpus (RAG)  +  private docs (RAG / Vectorless RAG)
   │
   ▼
[ Draft answer ]   ── grounded ONLY in retrieved evidence, with inline citations
   │
   ▼
[ Guardrail: compliance review ]  ── scores answer; no invented numbers; citations present?
   │           │
   │           └─ weak ──► [ Amend ] ──► re-check (capped)
   ▼
Cited answer  +  source list  +  audit log  (every step recorded)
```

Key product promises:
1. **Every claim is cited.** No citation → the answer is flagged or refused.
2. **It refuses gracefully.** "I don't have a source for that" beats a confident wrong answer — non-negotiable in finance.
3. **Everything is logged.** A full audit trail of what was retrieved, what was answered, and how the guardrail scored it.

---

## 4. Why this technology stack (the 7 pieces, mapped)

| Technology | Role in FinCopilot |
|---|---|
| **LLM Gateway** | One endpoint in front of all models — routing, fallback, cost tracking, key management. Lets us swap/upgrade models without touching app code. |
| **LangChain** | Component layer — prompts, retrievers, tool wiring, document loaders. |
| **LangGraph** | The orchestration brain — the stateful retrieve → draft → review → amend graph above, with loop caps and human-in-the-loop hooks. |
| **RAG** | Grounding answers in a regulatory corpus + uploaded documents (vector search). |
| **Vectorless RAG** | For **highly structured, auditable** documents — navigate the document's own tree/sections instead of fuzzy vector chunks. Better citations, no embedding drift. We compare it head-to-head with classic RAG. |
| **Guardrails** | Input checks (scope, PII, injection) + output checks (citations required, no invented numbers, compliance scoring). The trust layer. |
| **LLM Evaluation** | A labeled test set + LLM-as-judge to measure accuracy, citation coverage, and refusal correctness — so we can change models/prompts without silently regressing. |

---

## 5. Why now / why us
- The stack is finally mature enough that a small team can build a grounded, guardrailed assistant.
- We have a **warm fintech contact** as a design partner — the single biggest advantage (real pain, real data, real first user).
- The differentiator is **not novelty** — it's *trust + grounding + a specific vertical*. We win where generic tools are unsafe.

---

## 6. Explicit non-goals (what FinCopilot is NOT)
- ❌ Not a neobank, wallet, or anything that **moves or custodies money**.
- ❌ Not giving **regulated financial/investment advice to consumers**.
- ❌ Not a trading or credit-decisioning engine.
- ❌ Not a general chatbot — it **refuses out-of-scope questions** by design.

We stay firmly in **decision-support over documents**, where there's no license requirement and the moat is accuracy + auditability.

---

## 7. Open questions
**Resolved:** corpus = public RBI Digital Lending + KYC regulation (see §2). No
private data required to build the prototype.

Still open (for the pilot, not the build):
- Which of the contact's **internal workflows** maps onto this first? (e.g. vetting an LSP agreement, KYC process review)
- When/whether to layer their **private policies** on top of the public corpus.
- Which adjacent regulatory slice to expand to next (SEBI, payments, data).
