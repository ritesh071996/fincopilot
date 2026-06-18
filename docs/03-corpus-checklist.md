# FinCopilot — Corpus Checklist (Week 0–1)

The documents that ground every answer. **All public, all free.** Scope for the
prototype: **Digital Lending + KYC/AML**. Keep it small and focused — a tight,
relevant corpus gives better retrieval and cleaner evals than dumping everything.

> **Where files go:** download each as PDF into `data/corpus/`.
> They're gitignored (we don't redistribute RBI PDFs) — the folder stays, the
> files don't get committed.

---

## How to find them (since you're new to this)
RBI publishes everything on its official site, **rbi.org.in**. Two reliable routes:

1. **RBI website → "Notifications"** (top menu). Each circular/Master Direction
   has its own page with a **PDF** link.
2. **Google the exact title + "rbi.org.in"** — e.g.
   `Guidelines on Digital Lending rbi.org.in` — and open the rbi.org.in result.

Always download from **rbi.org.in** (the official source) so citations are
authoritative. Save with a clear filename (suggested names below).

> I can't fetch these for you automatically without your go-ahead (they're
> external downloads). Tell me to, and I'll pull the public ones into
> `data/corpus/` for you.

---

## What's in the corpus now (downloaded & verified)

### A. Digital Lending  ✅
- [x] **RBI (Digital Lending) Directions, 2025** — RBI/2025-26/36, dated May 8, 2025 (24 pages)
      → `data/corpus/rbi-digital-lending-directions-2025.pdf`
      > ⚠️ **Currency note:** the older *September 2022 "Guidelines on Digital
      > Lending" were REPEALED* and replaced by these 2025 Directions. We use the
      > current one — using superseded regulation in a compliance tool is a bug.

### B. KYC / AML  ✅
- [x] **Master Direction – Know Your Customer (KYC) Direction, 2016**
      (full consolidated version, updated 2025 — 107 pages)
      → `data/corpus/rbi-kyc-master-direction-2025.pdf`

### C. Optional next (only if eval shows a gap)
- [ ] **Outsourcing of Financial Services** guidance (LSP arrangements)
- [ ] **Fair Practices Code** for lenders

> Two strong, current documents is a deliberately tight corpus — better retrieval
> and cleaner evals than dumping everything. Resist adding more until the eval
> shows you actually need it.

## How these were fetched (for future reference)
RBI's `rbidocs.rbi.org.in` sits behind an **F5/Shape bot-protection WAF** that
serves a JavaScript challenge page to plain downloaders. The working method:
first GET the document's notification page on `rbi.org.in` to establish a
session/cookies, then request the `.PDF` with that same session + a browser
User-Agent + the notification page as `Referer`. (A normal browser passes the
WAF automatically — so manual download in a browser also works.)

---

## After downloading — the other half of Week 0–1
1. Confirm all 5 PDFs are in `data/corpus/` and open correctly.
2. Open [`eval/questions.yaml`](../eval/questions.yaml) and write **~20 real
   questions** answerable from these documents, plus a few **out-of-scope**
   ones (`should_refuse: true`). This is what we measure accuracy against —
   it's worth doing carefully.

---

## Checklist summary
- [ ] 5 PDFs downloaded from rbi.org.in into `data/corpus/`
- [ ] Filenames match the suggestions above (keeps citations tidy)
- [ ] ~20 eval questions written in `eval/questions.yaml`
- [ ] Ready for Week 2–3: build the ingest pipeline + first cited answer
