from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.customer import Customer


def create_conversation(
    db: Session,
    customer_id: int,
) -> Conversation:

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise ValueError("Customer not found.")

    conversation = Conversation(
        customer_id=customer_id,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation