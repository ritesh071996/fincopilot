"""Input guardrail: validate the question before processing.

Checks (Week 4-5):
  - scope:        is this actually a finance/compliance question we cover?
  - PII:          does the question leak personal/account data we should strip?
  - injection:    is the user trying to override the system prompt?

Returns a verdict; the agent refuses early if the question fails.
"""

from dataclasses import dataclass


@dataclass
class InputVerdict:
    allowed: bool
    reason: str = ""


def check_input(question: str) -> InputVerdict:
    """Validate an incoming question. STUB — implemented in Week 4-5."""
    raise NotImplementedError("Input guardrail lands in Week 4-5.")
