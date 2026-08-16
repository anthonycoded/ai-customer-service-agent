from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import (
    create_message,
    get_conversation_messages,
)


router = APIRouter(
    prefix="/conversations/{conversation_id}/messages",
    tags=["Messages"],
)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=201,
)
def create_message_endpoint(
    conversation_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_message(
            db,
            conversation_id,
            message_data.role,
            message_data.content,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

@router.get(
    "",
    response_model=list[MessageResponse],
)
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_conversation_messages(
            db,
            conversation_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )