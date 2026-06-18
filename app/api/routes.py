"""HTTP routes. Thin layer — receives the request, calls the agent, returns
the answer. No business logic lives here.

"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.answer import answer_question

router = APIRouter(prefix="/api/v1")


class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    citations: list[str] = []
    refused: bool = False


@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    """Ask a compliance question. Returns a cited answer (or a refusal)."""
    result = answer_question(req.question)
    return AskResponse(
        answer=result.answer,
        citations=result.citations,
        refused=result.refused,
    )
