import time
from typing import List, Optional
from fastapi import Security, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
import os
import base64
import json

class AuthGuard:
    def __init__(self, roles: Optional[List[str]] = None):
        self.roles = roles or []
        self.oauth2_scheme = HTTPBearer()

    def __call__(self, token: str = Security(HTTPBearer())):
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Unauthorized"
            )
        jwt_secret = os.getenv('JWT_SECRET_KEY_ACCESS', 'X9@Lq8^pM2B!R0YV7&WZJ5TQmF3Ko6D*')
        jwt_algorithm = os.getenv('JWT_ALGORITHM', 'HS256')

        try:
            print('ciao')
            decoded_token = jwt.decode(token.credentials, jwt_secret, algorithms=[jwt_algorithm])

        except JWTError:
            raise HTTPException(status_code=401, detail="Unauthorized")

      
        splitted: List[str] = token.credentials.split(".")
        token_payload_decoded = str(base64.b64decode(splitted[1] + "=="), "utf-8")
        payload: dict = json.loads(token_payload_decoded)
          # Decodifica payload
        exp = payload.get("expires_at")
        if exp is not None and time.time() > exp:
            raise HTTPException(status_code=401, detail="Token expired")
        # Controllo dei ruoli
        user_roles = payload.get("role", [])
        if self.roles and not any(role in user_roles for role in self.roles):
            raise HTTPException(status_code=403, detail="Forbidden")
        return payload  # Ritorna il payload del token
