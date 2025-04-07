import base64
import json
from typing import List
from asgiref.sync import sync_to_async
from fastapi.requests import Request


class TokenExtractor:
    @staticmethod
    async def extract_payload_from_request(req: Request) -> str:
        token: str = req.headers["Authorization"].split("Bearer")[1]
        splitted: List[str] = token.split(".")
        token_payload_decoded = str(base64.b64decode(splitted[1] + "=="), "utf-8")
        return json.loads(token_payload_decoded)
    
    @staticmethod
    def extract_token_from_request_sync(req: Request) -> str:
        token: str = req.headers["Authorization"].split("Bearer")[1]
        return token

    
    @staticmethod
    @sync_to_async
    def extract_user_id_from_request(req: Request) -> str:
        token: str = req.headers["Authorization"].split("Bearer")[1]
        splitted: List[str] = token.split(".")
        token_payload_decoded = str(base64.b64decode(splitted[1] + "=="), "utf-8")
        payload: dict = json.loads(token_payload_decoded)
        return payload["user_id"]