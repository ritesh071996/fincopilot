"""LLM Gateway — the single doorway for every model call.

Why this exists: we never call provider SDKs directly from the app. Everything
goes through here via LiteLLM, which exposes 100+ providers behind one
OpenAI-style call. In one place we get:
  - the ability to swap models via .env without touching app code
  - (later) provider routing + fallback and cost/token tracking

Embeddings are handled LOCALLY (app.ingest.embed_store), so this gateway is only
for text generation right now.
"""

import os
import time

import litellm
from litellm.exceptions import (
    APIConnectionError,
    InternalServerError,
    RateLimitError,
    ServiceUnavailableError,
    Timeout,
)

from app.config import settings

# Make provider keys available to litellm (it reads them from the environment).
if settings.openai_api_key:
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key
if settings.gemini_api_key:
    os.environ["GEMINI_API_KEY"] = settings.gemini_api_key

# Transient errors worth retrying: rate-limits (429) and server hiccups (503, etc.)
_TRANSIENT = (RateLimitError, ServiceUnavailableError, InternalServerError,
              APIConnectionError, Timeout)
_MAX_RETRIES = 5          # how many times to retry on a transient error
_BASE_DELAY = 6           # seconds; grows exponentially per retry


def complete(prompt: str, *, model: str | None = None, system: str | None = None) -> str:
    """Send a prompt to the configured model and return the text response.

    Retries automatically on rate-limit (429) errors with exponential backoff —
    the free Gemini tier is only a few requests/minute, so this keeps batch
    work (like the eval harness) from dying on a burst.
    """
    messages: list[dict] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    delay = _BASE_DELAY
    for attempt in range(_MAX_RETRIES + 1):
        try:
            response = litellm.completion(
                model=model or settings.llm_synthesis_model,
                messages=messages,
                timeout=60,
            )
            return response.choices[0].message.content
        except _TRANSIENT as e:
            if attempt == _MAX_RETRIES:
                raise
            print(f"[gateway] transient error ({type(e).__name__}); retrying in {delay}s "
                  f"(attempt {attempt + 1}/{_MAX_RETRIES})")
            time.sleep(delay)
            delay *= 2

if __name__ == "__main__":
    print(complete("Reply with exactly this text and nothing else: gateway works"))