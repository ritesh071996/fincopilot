"""Output guardrail: validate the drafted answer before it's shown.

Checks (Week 4-5):
  - citations-required:  every factual claim must map to a retrieved source
  - no-invented-numbers: any number in the answer must appear in a source
  - compliance score:    an LLM-as-reviewer rates the answer 1-5

If the answer fails, the agent's [amend] node rewrites it and we re-check
(capped). This is the core safety mechanism of FinCopilot.
"""

from dataclasses import dataclass


@dataclass
class OutputVerdict:
    passed: bool
    score: int          # 1-5
    issues: list[str]


def check_output(answer: str, chunks: list) -> OutputVerdict:
    """Validate a drafted answer against its sources. STUB — Week 4-5."""
    raise NotImplementedError("Output guardrail lands in Week 4-5.")
