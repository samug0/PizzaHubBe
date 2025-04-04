from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class SignInRequestDTO(BaseModel):
    email_or_username : str
    password : str


class SignUpRequestDTO(BaseModel):
    name : Annotated[str, Field(min_length=3, max_length=30)]
    last_name : Annotated[str, Field(min_length=3, max_length=30)]
    email : EmailStr
    username : Annotated[str, Field(min_length=4, max_length=14)]
    password : Annotated[str, Field(min_length=4, max_length=20)]
    #password: Annotated[str, Field(min_length=8, max_length=30, pattern=r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]+$")]
     # Mappa i parametri che vuoi usare nel backend
    class Config:
        # Usa l'alias per fare in modo che i dati vengano passati con i nomi giusti nel backend
        validate_by_name = True

class SignOutRequestDTO(BaseModel):
    refresh_token : str


class RefreshRequestDTO(BaseModel):
    refresh_token : str


class MeRequestDTO(BaseModel):
    refresh_token : str
