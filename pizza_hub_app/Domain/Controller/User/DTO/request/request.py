from typing import Optional
from pydantic import BaseModel, Field

class UpdateUserRequestDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=30)
    lastname: Optional[str] = Field(None, min_length=3, max_length=30)
    username: Optional[str] = Field(None, min_length=4, max_length=14)
    city: Optional[str] = Field(None, min_length=3, max_length=50)
    country: Optional[str] = Field(None, min_length=3, max_length=50)
    address: Optional[str] = Field(None, min_length=3, max_length=50)

    class Config:
        # Usa l'alias per fare in modo che i dati vengano passati con i nomi giusti nel backend
        validate_by_name = True