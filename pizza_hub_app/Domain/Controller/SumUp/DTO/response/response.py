from pydantic import BaseModel


class CreatePaymentIntentResponseDTO(BaseModel):
    client_secret : str