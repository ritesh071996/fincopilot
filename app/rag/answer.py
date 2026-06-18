"""Turn a question into a grounded, cited answer.

The first end-to-end slice: retrieve -> prompt the LLM with ONLY the retrieved
context -> return an answer plus citations. The real compliance guardrail +
amend loop comes later (Week 4-5); for now, grounding and refusal are enforced
by the prompt.
"""

from dataclasses import dataclass

from app.gateway import llm
from app.rag.retriever import RetrievedChunk, retrieve

REFUSAL = "I don't have a source for that in the provided regulation."

SYSTEM = (
    "You are FinCopilot, a financial compliance assistant. "
    "Answer ONLY using the provided context from RBI regulation. "
    "Every factual claim must be supported by the context, with inline [n] citations. "
    f"If the context does not contain the answer, reply exactly: '{REFUSAL}' "
    "Never invent numbers, clauses, or facts."
)


@dataclass
class Answer:
    answer: str
    citations: list[str]
    refused: bool


def _format_context(chunks: list[RetrievedChunk]) -> str:
    return "\n\n".join(
        f"[{i}] Source: {c.source}\n{c.text}" for i, c in enumerate(chunks, start=1)
    )


def answer_question(question: str) -> Answer:
    chunks = retrieve(question)
    context = _format_context(chunks)

    prompt = (
        f"Context from RBI regulation:\n\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer using only the context above, with inline [n] citations."
    )

    text = llm.complete(prompt, system=SYSTEM)
    refused = REFUSAL.lower() in text.lower()

    # De-duplicated list of sources we actually retrieved (skip if refused).
    citations: list[str] = []
    if not refused:
        for c in chunks:
            if c.source not in citations:
                citations.append(c.source)

    return Answer(answer=text, citations=citations, refused=refused)


if __name__ == "__main__":
    q = "Can loan disbursals be routed through the LSP's bank account?"
    a = answer_question(q)
    print("Q:", q)
    print("\nANSWER:\n", a.answer)
    print("\nREFUSED:", a.refused)
    print("CITATIONS:", a.citations)
