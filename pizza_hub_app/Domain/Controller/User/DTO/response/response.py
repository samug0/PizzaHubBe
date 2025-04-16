from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr

from pydantic import BaseModel


class UserResponseDTO(BaseModel):
    id: UUID
    name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    username: str
    city: Optional[str]
    country: Optional[str]
    address: Optional[str]
    created_at: datetime
    updated_at: datetime







class IngredientModel(BaseModel):
    id : UUID
    name : str
    price : float
    

class ProductInstanceModel(BaseModel):
    id : UUID
    product_id : UUID
    total_price : int
    product_name : str
    product_price : float
    ingredients : List[Optional[IngredientModel]]
    created_at: datetime
    updated_at: datetime

class CartModel(BaseModel):
    id : UUID
    product_instances : List[ProductInstanceModel]
    quantity : int
    created_at: datetime
    updated_at: datetime


class UserAggregatedResponseDTO(BaseModel):
    id: UUID
    name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    username: str
    city: Optional[str]
    country: Optional[str]
    address: Optional[str]
    phone_number : Optional[str]
    country : Optional[str]
    role : str
    cart : CartModel
    created_at: datetime
    updated_at: datetime

