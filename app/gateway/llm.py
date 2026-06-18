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
import litellm
from app.config import settings

# Make the Gemini key available to litellm (it reads GEMINI_API_KEY from the env).
if settings.gemini_api_key:
    os.environ["GEMINI_API_KEY"] = settings.gemini_api_key

def complete(prompt: str, *, model: str | None = None, system:str | None = None) -> str:
    """Send a prompt to the configured model and return the text response."""
    messages: list[dict] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = litellm.completion(
        model=model or settings.llm_synthesis_model,
        messages=messages,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print(complete("Reply with exactly this text and nothing else: gateway works"))