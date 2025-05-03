from uuid import UUID
from pydantic import BaseModel


class CreatePaymentIntentRequestDTO(BaseModel):
    amount : float
    user_id : UUID