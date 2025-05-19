import base64
import inspect
import json
import os
from jose import jwt
from jose import JWTError
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Callable, Awaitable
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.db.models.base import ModelBase
from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError
from pydantic import BaseModel
from pydantic import ValidationError
from django.http.request import HttpRequest
from pizza_hub_app.utils.logger.logger import AppLogger
from pizza_hub_app.utils.shared.token_extractor import TokenExtractor
import os
from fastapi.security import HTTPBearer
from typing import List
from pizza_hub_app.Domain.Controller.Auth.DTO.request.request import SignInRequestDTO


T = TypeVar("T")

logger = AppLogger(__name__)


class AbstractController(ABC):
    @abstractmethod
    def configure_routes(self):
        pass

    @abstractmethod
    def get_router(self):
        pass

    @staticmethod
    def response(message: dict):
        return JSONResponse(jsonable_encoder(message))

    def success_response(self, success: bool):
        return self.response({"success": success})

    @staticmethod
    def bad_request(detail):
        return HTTPException(status_code=400, detail=str(detail))

    @staticmethod
    def unauthorized(detail):
        if detail:
            return HTTPException(status_code=401, detail=str(detail))
        return HTTPException(status_code=401, detail="Invalid credentials")

    @staticmethod
    def forbidden():
        return HTTPException(status_code=403, detail="Invalid role")

    @staticmethod
    def not_found(detail):
        return HTTPException(status_code=404, detail=f"Not found: {str(detail)}")

    @staticmethod
    def conflict(detail):
        return HTTPException(status_code=409, detail=f"Conflict: {str(detail)}")

    @staticmethod
    def internal_server_error(detail):
        return HTTPException(status_code=500, detail=str(detail))

    

    

    async def execute_action(
        self, action: Callable[[], Awaitable[T]], model=ModelBase or None, pydantic_model=BaseModel
    ) -> Awaitable[T]:
        async def wrapper():
            try:
                return await action()
            except ValidationError as e:
                logger.error(
                    f"A Validation error occurred in {pydantic_model} model. Error occurred in class: {self._get_class_name()} --> DETAIL: {str(e)}"
                )
                raise self.bad_request(e)
            except ValueError as e:
                raise self.bad_request(e)
            except IntegrityError as e:
                logger.error(
                    f"An integrity occurred in {model} model. Error occurred in class: {self._get_class_name()} --> DETAIL: {str(e)}"
                )
                raise self.bad_request(e)
            except ObjectDoesNotExist as e:
                logger.error(
                    f"Object on {model} model not found! Error occurred in class: {self._get_class_name()}"
                )
                raise self.not_found(e)
            
            except HTTPException as e:
                if e.status_code == 404:
                    logger.error(f"Class '{self._get_class_name}' not found")
                if e.status_code == 409:
                    logger.error(f"Class '{self._get_class_name}' conflict error --> DETAIL {str(e)}")
                    raise self.conflict(e)
            except Exception as e:
                logger.critical(
                    f"Request Error not detected! Error occurred in class: {self._get_class_name()} --> DETAIL: {str(e)}"
                )
                raise self.internal_server_error(e)
        return await wrapper()

    def _get_class_name(self):
        frame = inspect.currentframe()
        outer_frames = inspect.getouterframes(frame)

        for outer_frame in outer_frames:
            if "self" in outer_frame.frame.f_locals:
                instance = outer_frame.frame.f_locals["self"]
                if isinstance(instance, AbstractController):
                    return instance.__class__.__name__
        return "Unknown"
            

