"""LangGraph agent: retrieve -> generate -> compliance-review -> (amend)* -> answer.

If the output guardrail rejects a draft, the reviewer's issues are fed back and
the answer is rewritten, up to MAX_ATTEMPTS. If it still fails, the agent
refuses rather than show an ungrounded answer.
"""

from typing import TypedDict

from langgraph.graph import START, END, StateGraph

from app.gateway import llm
from app.guardrails.output_guard import check_output
from app.rag.retriever import retrieve

MAX_ATTEMPTS = 2

DRAFT_SYSTEM = (
    "You are FinCopilot, a financial compliance assistant. "
    "Answer ONLY using the provided context from RBI regulation, with inline [n] citations. "
    "Never invent numbers, clauses, or facts. Be precise and concise."
)


class AgentState(TypedDict, total=False):
    question: str
    context: str
    citations: list[str]
    draft: str
    issues: list[str]
    score: int
    passed: bool
    attempts: int
    answer: str
    refused: bool


def retrieve_node(state: AgentState) -> dict:
    chunks = retrieve(state["question"])
    context = "\n\n".join(
        f"[{i}] Source: {c.source}\n{c.text}" for i, c in enumerate(chunks, start=1)
    )
    citations: list[str] = []
    for c in chunks:
        if c.source not in citations:
            citations.append(c.source)
    return {"context": context, "citations": citations, "attempts": 0, "issues": []}


def generate_node(state: AgentState) -> dict:
    feedback = ""
    if state.get("issues"):
        feedback = (
            "\nYour previous answer had these problems: "
            + "; ".join(state["issues"])
            + ". Fix them using only the context."
        )
    prompt = (
        f"CONTEXT:\n{state['context']}\n\n"
        f"QUESTION: {state['question']}\n{feedback}\n\n"
        "Answer using only the context above, with inline [n] citations."
    )
    draft = llm.complete(prompt, system=DRAFT_SYSTEM)
    return {"draft": draft, "attempts": state.get("attempts", 0) + 1}


def review_node(state: AgentState) -> dict:
    verdict = check_output(state["draft"], state["context"])
    return {"passed": verdict.passed, "score": verdict.score, "issues": verdict.issues}


def finalize_node(state: AgentState) -> dict:
    if state.get("passed"):
        return {"answer": state["draft"], "refused": False}
    return {
        "answer": "I could not produce a sufficiently grounded answer from the regulation.",
        "refused": True,
    }


def route_after_review(state: AgentState) -> str:
    if state.get("passed"):
        return "finalize"
    if state.get("attempts", 0) >= MAX_ATTEMPTS:
        return "finalize"
    return "generate"


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("retrieve", retrieve_node)
    g.add_node("generate", generate_node)
    g.add_node("review", review_node)
    g.add_node("finalize", finalize_node)

    g.add_edge(START, "retrieve")
    g.add_edge("retrieve", "generate")
    g.add_edge("generate", "review")
    g.add_conditional_edges("review", route_after_review,
                            {"generate": "generate", "finalize": "finalize"})
    g.add_edge("finalize", END)
    return g.compile()


# Build once and reuse.
_graph = build_graph()


def run_agent(question: str) -> dict:
    final = _graph.invoke({"question": question})
    return {
        "answer": final["answer"],
        "citations": final.get("citations", []) if not final.get("refused") else [],
        "refused": final.get("refused", False),
        "score": final.get("score"),
        "attempts": final.get("attempts"),
    }


if __name__ == "__main__":
    for q in [
        "Can loan disbursals be routed through the LSP's bank account?",
        "What is the cap on a Default Loss Guarantee?",
    ]:
        print("Q:", q)
        r = run_agent(q)
        print("  refused:", r["refused"], "| score:", r["score"], "| attempts:", r["attempts"])
        print("  answer:", r["answer"][:200])
        print("  citations:", r["citations"])
        print()
