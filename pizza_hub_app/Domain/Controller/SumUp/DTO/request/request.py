from uuid import UUID
from pydantic import BaseModel


class CreatePaymentIntentRequestDTO(BaseModel):
    user_id : UUID



