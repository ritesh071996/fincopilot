"""LangGraph agent definition.

The graph (built in Week 4-5):

    START
      |
      v
    [input_guard]  --unsafe/out-of-scope-->  REFUSE
      |
      v
    [retrieve]      pull cited chunks (rag.retriever)
      |
      v
    [draft]         write an answer grounded ONLY in retrieved chunks
      |
      v
    [compliance]    score it; citations present? invented numbers? (guardrails)
      |   |
      |   +--weak--> [amend] --> back to [compliance]  (capped at N tries)
      v
    [answer]        return answer + citations + audit log

State carried between nodes: question, retrieved chunks, draft, scores, attempts.
"""

from typing import TypedDict


class AgentState(TypedDict, total=False):
    question: str
    chunks: list          # retrieved evidence
    draft: str
    citations: list
    compliance_score: int
    attempts: int
    refused: bool
    answer: str


def build_graph():
    """Construct and compile the LangGraph StateGraph.

    STUB — implemented in Week 4-5.
    """
    raise NotImplementedError("LangGraph agent lands in Week 4-5.")
