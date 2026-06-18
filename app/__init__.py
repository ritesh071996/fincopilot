"""FinCopilot — a document-grounded financial compliance & research copilot.

Package layout (each sub-package maps to one piece of the stack):

    config.py      application settings (reads .env)
    gateway/       LLM Gateway — one place all model calls go through
    ingest/        load -> chunk -> embed -> store the regulatory corpus
    rag/           retrieval (vector RAG now; vectorless RAG later)
    graph/         LangGraph agent: retrieve -> draft -> guardrail -> amend
    guardrails/    input + output safety / compliance checks
    api/           FastAPI routes

Built incrementally — see ../docs/02-timeline.md for which week each piece lands.
"""

# Windows fix: load the SSL/OpenSSL stack BEFORE torch (pulled in by embeddings).
# If SSL initializes AFTER torch, later HTTPS calls (e.g. the Gemini API) segfault
# with an access violation. This package __init__ runs before any submodule that
# imports torch, so it's the right place. See PROJECT-MEMORY.md.
import ssl

ssl.create_default_context()

__version__ = "0.0.1"
