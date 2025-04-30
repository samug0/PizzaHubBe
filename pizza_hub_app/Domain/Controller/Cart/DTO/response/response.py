from pydantic import BaseModel
from uuid import UUID
from typing import List
from datetime import datetime


class IngredientsModel(BaseModel):
    id : UUID
    name : str 
    price : float

class ProductInstanceModel(BaseModel):
   id : UUID
   name : str
   total_price : float
   product_name : str
   ingredients : List[IngredientsModel] | None


class CartResponseDTO(BaseModel):
    id : UUID
    product_instances: List[ProductInstanceModel]
    quantity: int
    total: float
    created_at: datetime
    updated_at: datetime