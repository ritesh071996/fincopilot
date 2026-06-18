"""Retrieve the most relevant corpus chunks for a question.

Returns chunks WITH their source metadata so the answer can cite them.
"""

from dataclasses import dataclass

from app.config import settings
from app.ingest.embed_store import get_vectorstore

@dataclass
class RetrievedChunk:
    text:str
    source:str      # citable reference, e.g. "RBI ... , P..5"
    score:float     # lower = more similar (Chroma distance)

# Load the vector store once and reuse it (avoids reloading the model each call)
_store = None

def _get_store():
    global _store
    if _store is None:
        _store = get_vectorstore()
    return _store

def retrieve(question: str, top_k: int | None = None) -> list[RetrievedChunk]:
    """Return the top-k most relevant chunks for the question."""
    k = top_k or settings.retrieval_top_k
    results = _get_store().similarity_search_with_score(question, k=k)

    chunks: list[RetrievedChunk] = []
    for doc, score in results:
        meta = doc.metadata
        source = f"{meta.get('source', '?')}, p.{meta.get('page', '?')}"
        chunks.append(RetrievedChunk(text=doc.page_content, source=source, score=float(score)))
    return chunks

if __name__ == "__main__":
    q = "Does a lender need a written agreement with a Lending Service Provider?"
    print("Q:", q, "\n")
    for c in retrieve(q):
        print(f"[{c.score:.3f}] {c.source}")
        print("  ", c.text[:160].replace("\n", " "))
        print()