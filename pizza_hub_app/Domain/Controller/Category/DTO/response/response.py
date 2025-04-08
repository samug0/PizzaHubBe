from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class CategoryResponseDTO(BaseModel):
    id : UUID
    name : str
    description : Optional[str]
    created_at : datetime
    updated_at : datetime