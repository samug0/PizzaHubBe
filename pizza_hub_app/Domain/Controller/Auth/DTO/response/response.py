from pydantic import BaseModel, EmailStr
from typing import Optional

class SignInResponseDTO(BaseModel):
    access_token : str
    refresh_token : str


class RefreshResponseDTO(BaseModel):
    access_token : str
    refresh_token : str


class MeResponseDTO(BaseModel):
    name : str
    last_name : str
    email : EmailStr
    username : str
    city : Optional[str]
    status : str
    phone_number : Optional[str]
    country : Optional[str]
    address : Optional[str]
    profile_image : Optional[str]
    role : str