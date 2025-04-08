from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class ProductResponseDTO(BaseModel):
    id : UUID
    name : str
    price : float
    description : Optional[str]
    ingredients : Optional[List[str]]
    is_available : bool
    created_at : datetime
    updated_at : datetime