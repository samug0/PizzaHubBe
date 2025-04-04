from functools import partial
from pizza_hub_app.Domain.Controller.Auth.guard.auth_guard import AuthGuard
from pizza_hub_app.Domain.Controller.abstract_controller import AbstractController
from fastapi import APIRouter, Depends
from typing import Mapping
from pizza_hub_app.Domain.Controller.Auth.DTO.request.request import MeRequestDTO, SignInRequestDTO, SignUpRequestDTO, SignOutRequestDTO, RefreshRequestDTO
from pizza_hub_app.Domain.Controller.Auth.DTO.response.response import SignInResponseDTO, RefreshResponseDTO, MeResponseDTO
from pizza_hub_app.utils.logger.logger import AppLogger
from pizza_hub_app.Domain.Service.Auth.service import AuthService
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer
from typing import Annotated


logger = AppLogger(__name__)

security = HTTPBasic()


class AuthController(AbstractController):

    def __init__(self):
        self.__router = APIRouter(prefix="/auth", tags=["Auth"])
        self.__auth_service = AuthService()
        self.configure_routes()

    def get_router(self):
        return self.__router


    def configure_routes(self):
        self.__router.post("/sign-in", status_code=200, response_model=SignInResponseDTO)(self.sign_in)
        self.__router.post("/sign-up", status_code=201, response_model=Mapping[str, bool])(self.sign_up)
        self.__router.post("/sign-out", status_code=200, response_model=Mapping[str, bool])(self.sign_out)
        self.__router.post("/refresh", status_code=200, response_model=RefreshResponseDTO)(self.refresh)
        self.__router.post("/me", status_code=200, response_class=JSONResponse, dependencies=[Depends(AuthGuard(['ADMIN', 'USER']))])(self.me)


    async def sign_in(self, request: SignInRequestDTO):
        async def action():
            tokens : SignInResponseDTO = await self.__auth_service.sign_in(request)
            return JSONResponse(tokens.model_dump(), 200)
        return await self.execute_action(action)
    

    
    async def sign_up(self, request: SignUpRequestDTO):
        async def action():
            response: bool = await self.__auth_service.sign_up(request)
            if response == True:
                return self.success_response(True)
            else:
                return self.success_response(False)
        return await self.execute_action(action)
    

    async def sign_out(self, request: SignOutRequestDTO):
        async def action():
            response : bool = await self.__auth_service.sign_out(request)
            if response == True:
                return self.success_response(True)
            else:
                return self.success_response(False)
        return await self.execute_action(action)
    

    async def refresh(self, request: RefreshRequestDTO):
        async def action():
            response : RefreshResponseDTO = await self.__auth_service.refresh(request)
            return JSONResponse(response.model_dump(), 200)
        return await self.execute_action(action)
    

    async def me(self, request: MeRequestDTO):
        async def action():
            response : MeResponseDTO = await self.__auth_service.me(request)
            return JSONResponse(response.model_dump(), 200)
        return await self.execute_action(action)


    