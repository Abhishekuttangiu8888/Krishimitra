
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.integrations.gemini import (
    generate_reply,
    GeminiAPIError,
)

router = APIRouter(
    prefix="/chat",
    tags=["AI Chatbot"],
)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=5000)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)

    history: list[ChatMessage] = Field(
        default_factory=list,
        max_length=12,
    )


class ChatResponse(BaseModel):
    success: bool
    reply: str


@router.post("/message", response_model=ChatResponse)
def chat_message(request: ChatRequest):

    try:
        history = [
            item.model_dump()
            for item in request.history
        ]

        reply = generate_reply(
            message=request.message,
            history=history,
        )

        return ChatResponse(
            success=True,
            reply=reply,
        )

    except GeminiAPIError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong. Please try again.",
        )
