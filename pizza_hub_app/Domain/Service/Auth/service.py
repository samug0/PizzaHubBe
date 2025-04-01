from pizza_hub_app.Domain.Service.abstract_service import AbstractService
from pizza_hub_app.Domain.Controller.Auth.DTO.request.request import SignInRequestDTO, SignUpRequestDTO
from pizza_hub_app.Domain.Controller.Auth.DTO.response.response import SignInResponseDTO
from pizza_hub_app.Domain.Service.User.service import UserService
from pizza_hub_app.utils.logger.logger import AppLogger
from fastapi.exceptions import HTTPException
from datetime import datetime, timedelta
import pytz
import os
from jose import JWTError, jwt
from django.contrib.auth.hashers import make_password, check_password
from pizza_hub_app.models import Role, RoleType, User, UserStatus
from asgiref.sync import sync_to_async


logger = AppLogger(__name__)

def get_expiration_time(hours: int):
    return datetime.now(tz=pytz.utc) + timedelta(hours=hours)


class AuthService(AbstractService):

    def __init__(self):
       super().__init__()
       self.__user_service = UserService()

    async def sign_in(self, req : SignInRequestDTO):
        validated_data : dict = SignInRequestDTO(**req.model_dump()).__dict__
        user = await self.__user_service.get_user_by_email(validated_data.get('email_or_username'))

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
            return SignInResponseDTO(**tokens_dict)

    async def sign_up(self, req: SignUpRequestDTO):
        validated_data : dict = SignUpRequestDTO(**req.model_dump()).__dict__
        user_found_email = await self.__user_service.get_user_by_email(validated_data.get('email'))
        if user_found_email:
            raise HTTPException(409, 'User already registered')
        user_found_username = await self.__user_service.get_user_by_username(validated_data.get('username'))
        if user_found_username:
            raise HTTPException(409, 'User already registered')
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
    
        payload_refresh = {'expires_at': expires_at_refresh}
        # print('ciao')
        access_token = jwt.encode(payload_access, os.getenv('JWT_SECRET_KEY_ACCESS', 'X9@Lq8^pM2B!R0YV7&WZJ5TQmF3Ko6D*'), os.getenv('JWT_ALGORITHM', 'HS256')) 
        refresh_token = jwt.encode(payload_refresh, os.getenv('JWT_SECRET_KEY_ACCESS', 'X9@Lq8^pM2B!R0YV7&WZJ5TQmF3Ko6D*'), os.getenv('JWT_ALGORITHM', 'HS256'))
        return {'access_token': access_token, 'refresh_token': refresh_token}