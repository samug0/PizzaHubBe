from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class ProductResponseDTO(BaseModel):
    id : UUID
    name : str
    price : float
    description : Optional[str]
    images : List[dict] | None
    product_categories : List[dict] | None
    ingredients: List[dict] | None
    is_available : bool
    created_at : datetime
    updated_at : datetime