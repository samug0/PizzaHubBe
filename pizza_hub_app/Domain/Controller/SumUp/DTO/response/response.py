from pydantic import BaseModel


class CreatePaymentIntentResponseDTO(BaseModel):
    payment_url : str