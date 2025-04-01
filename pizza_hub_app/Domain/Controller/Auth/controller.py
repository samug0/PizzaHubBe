from pizza_hub_app.Domain.Controller.abstract_controller import AbstractController
from fastapi import APIRouter
from typing import Mapping
from pizza_hub_app.Domain.Controller.Auth.DTO.request.request import SignInRequestDTO, SignUpRequestDTO
from pizza_hub_app.Domain.Controller.Auth.DTO.response.response import SignInResponseDTO
from pizza_hub_app.utils.logger.logger import AppLogger
from pizza_hub_app.Domain.Service.Auth.service import AuthService
from fastapi.responses import JSONResponse

logger = AppLogger(__name__)


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

    async def sign_in(self, request: SignInRequestDTO):
        async def action():
            tokens : SignInResponseDTO = await self.__auth_service.sign_in(request)
            return JSONResponse(tokens.model_dump(), 200)
        return await self.execute_action(action)
    

    
    async def sign_up(self, request: SignUpRequestDTO):
        async def action():
            response = await self.__auth_service.sign_up(request)
            if response == True:
                return self.success_response(True)
            else:
                return self.success_response(False)
        return await self.execute_action(action)