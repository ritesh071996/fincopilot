"""Central configuration. All settings come from environment variables / .env.

We never hardcode secrets or model names in code — they live in .env so we can
change models and providers without editing the app (that's the whole point of
the LLM Gateway).
"""

# Load HuggingFace models from the local cache only — never over the network.
# On this Windows machine an SSL call AFTER torch is loaded segfaults (a torch
# DLL clash), so embeddings MUST load offline. Models are pre-downloaded once
# via huggingface_hub (without torch). See PROJECT-MEMORY.md. Set before any
# HuggingFace import happens.
import os

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project paths -------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
CORPUS_DIR = DATA_DIR / "corpus"          # raw RBI PDFs go here
VECTORSTORE_DIR = DATA_DIR / "vectorstore"  # the local Chroma index lives here


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --- LLM Gateway -------------------------------------------------------
    # We route every model call through LiteLLM. These names are the model
    # the gateway should use; swap them in .env, not in code.
    # NOTE: defaults pinned during Week 6-7 (gateway) once verified current.
    llm_synthesis_model: str = "gemini/gemini-2.5-flash-lite"   # Gemini lite via litellm
    llm_extraction_model: str = "gemini/gemini-2.5-flash-lite"  # same for now
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    openai_api_key: str = ""        # legacy; unused now
    gemini_api_key: str = ""        # reads GEMINI_API_KEY from .env (free Gemini key)
    # add other provider keys here as we wire them in (anthropic, ...)

    # --- Retrieval ---------------------------------------------------------
    chunk_size: int = 1000
    chunk_overlap: int = 150
    retrieval_top_k: int = 5

    # --- App ---------------------------------------------------------------
    app_name: str = "FinCopilot"
    debug: bool = True


settings = Settings()
