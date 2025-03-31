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