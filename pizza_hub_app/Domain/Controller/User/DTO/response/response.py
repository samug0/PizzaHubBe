from datetime import datetime
from typing import Optional
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


class CartModel(BaseModel):
    id : UUID
    user_id : UUID
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

