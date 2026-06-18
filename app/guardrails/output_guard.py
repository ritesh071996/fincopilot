"""Output guardrail: validate a drafted answer against its sources.

The drafter writes the answer; this is a separate, skeptical reviewer that
checks it against ONLY the retrieved context — every claim supported? any
invented numbers? It returns a structured verdict so the agent can accept the
answer or send it back to be amended. This is the core safety layer.
"""

import json
from dataclasses import dataclass

from app.gateway import llm

REVIEWER_SYSTEM = (
    "You are a strict compliance reviewer for a financial regulatory assistant. "
    "You are given CONTEXT (excerpts from RBI regulation) and an ANSWER. "
    "Checking ONLY against the context, assess: "
    "(1) is every factual claim in the answer supported by the context? "
    "(2) does the answer state any number, date, percentage, or clause NOT in the context? "
    "(3) is the answer grounded and safe to show? "
    'Respond with ONLY JSON: {"score": <1-5>, "grounded": <true|false>, "issues": ["..."]}. '
    "score 5 = fully grounded, no issues; 1 = ungrounded or fabricated."
)

@dataclass
class OutputVerdict:
    passed: bool
    score: int      # 1-5
    issues: list[str]

def _extract_json(raw: str) -> dict:
    """Pull the JSON object out of the model's reply (it may add fences/prose)."""
    start, end = raw.find("{"), raw.rfind("}")
    return json.loads(raw[start : end + 1])

def check_output(answer:str, context:str) -> OutputVerdict:
    """Review an answer against its context. Fails safe if it can't be verified."""
    prompt = f"CONTEXT:\n{context}\n\nANSWER:\n{answer}\n\nReturn the JSON verdict."
    raw = llm.complete(prompt, system=REVIEWER_SYSTEM)

    try:
        data = _extract_json(raw)
    except Exception:
        return OutputVerdict(passed=False, score=1, issues=["could not parse reviewer output"])
    
    score = int(data.get("score", 1))
    grounded = bool(data.get("grounded", False))
    issues = data.get("issues") or []
    return OutputVerdict(passed=grounded and score >= 4, score=score, issues=issues)

if __name__ == "__main__":
    context = "The DLG cover shall not exceed five per cent (5%) of the total amount disbursed."
    good = "The DLG cover cannot exceed 5% of the total amount disbursed."
    bad = "The DLG cover cannot exceed 20% of the disbursed portfolio."  # invented number

    print("GOOD:", check_output(good, context))
    print("BAD :", check_output(bad, context))