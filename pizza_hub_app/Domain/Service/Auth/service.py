import asyncio
import base64
import json
import time
from typing import List, Optional
from fastapi import Request
from pizza_hub_app.Domain.Service.abstract_service import AbstractService
from pizza_hub_app.Domain.Controller.Auth.DTO.request.request import MeRequestDTO, SignInRequestDTO, SignUpRequestDTO, SignOutRequestDTO, RefreshRequestDTO
from pizza_hub_app.Domain.Controller.Auth.DTO.response.response import SignInResponseDTO, RefreshResponseDTO, MeResponseDTO
from pizza_hub_app.Domain.Service.User.service import UserService
from pizza_hub_app.utils.logger.logger import AppLogger
from fastapi.exceptions import HTTPException
from datetime import datetime, timedelta
import pytz
import os
from jose import ExpiredSignatureError, JWTError, jwt
from django.contrib.auth.hashers import make_password, check_password
from pizza_hub_app.models import Role, RoleType, User, UserStatus
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from pizza_hub_app.utils.shared.token_extractor import TokenExtractor


logger = AppLogger(__name__)

def get_expiration_time(hours: int):
    return datetime.now(tz=pytz.utc) + timedelta(hours=hours)


class AuthService(AbstractService):

    def __init__(self):
       super().__init__()
       self.__user_service = UserService()

    async def sign_in(self, req : SignInRequestDTO):
        validated_data : dict = SignInRequestDTO(**req.model_dump()).__dict__
        user = await self.__user_service.get_user_by_email_or_username(validated_data.get('email_or_username'))

        if not user:
            logger.error(f'User with email "{validated_data.get('email_or_username')}" not authorized!')
            raise HTTPException(401, 'Not Authorized')
        
        if user.status != UserStatus.ACTIVE:
            logger.error(f'User with email "{validated_data.get('email_or_username')}" has account not active!')
            raise HTTPException(401, 'Not Authorized')
       
        cripted_password = make_password(validated_data.get('password'))
        #print('ciao', check_password(validated_data.get('password'), cripted_password))
        if not check_password(validated_data.get('password'), cripted_password):
            logger.error(f'User with email "{validated_data.get('email_or_username')}" not authorized!')
            raise HTTPException(401, 'Not Authorized')
        else:
            expires_at_access = datetime.now(tz=pytz.utc) + timedelta(hours=1)
            expires_at_refresh = datetime.now(tz=pytz.utc) + timedelta(hours=2) 
            expires_at_access_ms = int(expires_at_access.timestamp() * 1000)
            expires_at_refresh_ms = int(expires_at_refresh.timestamp() * 1000)
            tokens_dict : dict = await self.generate_tokens(user, expires_at_access_ms, expires_at_refresh_ms)
            user.refresh_token = tokens_dict.get('refresh_token')
            await user.asave()
            return SignInResponseDTO(**tokens_dict)

    async def sign_up(self, req: SignUpRequestDTO):
        validated_data : dict = SignUpRequestDTO(**req.model_dump()).__dict__
        user_found_email = await self.__user_service.get_user_by_email(validated_data.get('email'))
        if user_found_email:
            raise HTTPException(409, 'Email already registered')
        user_found_username = await self.__user_service.get_user_by_username(validated_data.get('username'))
        if user_found_username:
            raise HTTPException(409, 'Username already registered')
        role_user : Role = await Role.objects.aget(name=RoleType.USER)
        validated_data['role_id'] = role_user.id
        response = True if await self.repository_accessor.user_repository.create(validated_data) else False
        if response == True:
            return True
    
    @sync_to_async
    def generate_tokens(self, user: User, expires_at_access: int, expires_at_refresh: int)-> dict:
        payload_access = {
                 'user_id': str(user.id),
                 'role': user.role.name,
                 'expires_at': expires_at_access
            }
    
        payload_refresh = {'exp': expires_at_refresh}
        # print('ciao')
        access_token = jwt.encode(payload_access, os.getenv('JWT_SECRET_KEY_ACCESS', 'X9@Lq8^pM2B!R0YV7&WZJ5TQmF3Ko6D*'), os.getenv('JWT_ALGORITHM', 'HS256')) 
        refresh_token = jwt.encode(payload_refresh, os.getenv('JWT_SECRET_KEY_REFRESH', 'R9&Xp@2Lq8^M!B0YV7WZJ5TQmF3Ko6D*'), os.getenv('JWT_ALGORITHM', 'HS256'))
        return {'access_token': access_token, 'refresh_token': refresh_token}
    

    @sync_to_async
    def validate_refresh_exp(self, refresh_token: str) -> bool:
        secret_key_refresh = os.getenv('JWT_SECRET_KEY_REFRESH', 'R9&Xp@2Lq8^M!B0YV7WZJ5TQmF3Ko6D*')
        parts = refresh_token.split(".")
        if len(parts) != 3:
            raise HTTPException(status_code=401, detail="Unauthorized: Token malformato")

        try:
            # ✅ Decodifica manuale del payload senza verificare la firma
            payload_base64 = parts[1]
            
            # Assicuriamoci che la lunghezza sia un multiplo di 4 per la decodifica Base64
            payload_base64 += "=" * (-len(payload_base64) % 4)
            
            token_payload_decoded = base64.urlsafe_b64decode(payload_base64).decode("utf-8")
            payload: dict = json.loads(token_payload_decoded)
            jwt.decode(refresh_token, secret_key_refresh, ['HS256'])
            exp: Optional[int] = payload.get("exp")
            if exp is not None and time.time() > exp:
                return False  # Token scaduto
            return True  # Token valido

        except ExpiredSignatureError:
            return False

        except JWTError as e:
            return False

    

    async def sign_out(self, request: SignOutRequestDTO) -> bool:
        validated_data = SignOutRequestDTO(**request.model_dump()).__dict__
        user : User = await self.__user_service.get_user_by_refresh_token(validated_data.get('refresh_token'))
        user.refresh_token = None
        return True
    

    async def refresh(self, request: RefreshRequestDTO) -> RefreshResponseDTO:
        validated_data = RefreshRequestDTO(**request.model_dump()).__dict__
        user : User = await self.__user_service.get_user_by_refresh_token(validated_data.get('refresh_token'))
        has_valid_refresh = await self.validate_refresh_exp(validated_data.get('refresh_token'))
        if has_valid_refresh == True:
            expires_at_access = datetime.now(tz=pytz.utc) + timedelta(hours=1)
            expires_at_refresh = datetime.now(tz=pytz.utc) + timedelta(hours=2) 
            expires_at_access_ms = int(expires_at_access.timestamp() * 1000)
            expires_at_refresh_ms = int(expires_at_refresh.timestamp() * 1000)
            tokens_dict : dict = await self.generate_tokens(user, expires_at_access_ms, expires_at_refresh_ms)
            response = {
                'access_token':tokens_dict.get('access_token'),
                'refresh_token': validated_data.get('refresh_token')
            }
            return RefreshResponseDTO(**response)
        elif user and has_valid_refresh == False:
            expires_at_access = datetime.now(tz=pytz.utc) + timedelta(hours=1)
            expires_at_refresh = datetime.now(tz=pytz.utc) + timedelta(hours=2) 
            expires_at_access_ms = int(expires_at_access.timestamp() * 1000)
            expires_at_refresh_ms = int(expires_at_refresh.timestamp() * 1000)
            tokens_dict : dict = await self.generate_tokens(user, expires_at_access_ms, expires_at_refresh_ms)
            user.refresh_token = tokens_dict.get('refresh_token')
            await user.asave()
            return RefreshResponseDTO(**tokens_dict)
        else:
            raise ObjectDoesNotExist()
    

    async def me(self, request: MeRequestDTO) ->MeResponseDTO:
        validated_data = MeRequestDTO(**request.model_dump()).__dict__
        user : User = await self.repository_accessor.user_repository.get_by_refresh_token(validated_data.get('refresh_token'))
        is_valid_refresh_token : bool =await self.validate_refresh_exp(validated_data.get('refresh_token'))
        print(is_valid_refresh_token) 
        if user and is_valid_refresh_token == True:
            role_name = await asyncio.get_running_loop().run_in_executor(None, lambda: user.role.name)
            user_data = {
                'name': user.name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
                'city': user.city,
                'status' : user.status,
                'city': user.city,
                'phone_number': user.phone_number,
                'country': user.country,
                'address': user.address,
                'profile_image': str(user.profile_image),
                'role': role_name
            }
            return MeResponseDTO(**user_data)
        else:
            raise HTTPException(401, 'Unauthorized')

