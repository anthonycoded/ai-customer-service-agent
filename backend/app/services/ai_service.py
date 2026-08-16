from sqlalchemy.orm import Session

from app.ai.ollama_service import OllamaService
from app.ai.prompts import SYSTEM_PROMPT
from app.services.message_service import (
    create_message,
    get_conversation_messages,
)


class AIService:
    def __init__(self):
        self.llm = OllamaService()

    def generate_response(
        self,
        db: Session,
        conversation_id: int,
    ):
        messages = get_conversation_messages(
            db,
            conversation_id,
        )

        llm_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        for message in messages:
            llm_messages.append(
                {
                    "role": message.role,
                    "content": message.content,
                }
            )

        response = self.llm.generate_response(
            llm_messages
        )

        return create_message(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=response,
        )