from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class IngredientResponseDTO(BaseModel):
    id : UUID
    name : str
    price : float
    created_at : datetime
    updated_at : datetime