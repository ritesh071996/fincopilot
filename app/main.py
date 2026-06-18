"""FastAPI entry point.

Run locally:
    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/docs for the auto-generated API docs.
"""

from fastapi import FastAPI

from app.config import settings
from app.api.routes import router

app = FastAPI(
    title=settings.app_name,
    description="Document-grounded financial compliance & research copilot.",
    version="0.0.1",
)

app.include_router(router)


@app.get("/health")
def health() -> dict:
    """Liveness check — confirms the server is up."""
    return {"status": "ok", "app": settings.app_name}
