from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

API_CATEGORY = "Auth"

# 2행 들여쓰기로는 PEP8 E121에 걸린다는데 이유를 모르겠다.
authroization_header = {
    "Autorization": {
        "description": "Autorization HTTP header with JWT access token, \
          like: Autorization: Bearer header.payload.signature",
        "in": "header",
        "type": "string",
        "required": True
    }
} 

from .user import *
