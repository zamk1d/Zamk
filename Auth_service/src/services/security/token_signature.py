from http.client import HTTPException
from uuid import uuid4

import jwt
import datetime
from fastapi import HTTPException

from src.config.custom_exceptions import MissingSubClaimError
from src.config.settings import settings

"""Tokens"""

with open("private_key.pem", "rb") as f:
    PRIVATE_KEY = f.read()

with open("public_key.pem", "rb") as f:
    PUBLIC_KEY = f.read()

def create_jwt(payload: dict, access_exp_minutes: int = settings.att, refresh_exp_days: int = settings.rtt) -> dict:
    now = datetime.datetime.now(datetime.timezone.utc)

    if "sub" not in payload.keys():
        raise MissingSubClaimError("'sub' claim is required in payload")

    access_payload = payload.copy()
    access_payload.update({
        "exp": int((now + datetime.timedelta(minutes=access_exp_minutes)).timestamp()),
        "type": "access"
    })
    access_token = jwt.encode(access_payload, PRIVATE_KEY, algorithm="RS256")

    refresh_payload = {"sub": payload.get("sub")}
    jti = str(uuid4())
    refresh_payload.update({
        "exp": int((now + datetime.timedelta(minutes=refresh_exp_days)).timestamp()),
        "type": "refresh",
        "jti": jti
    })
    refresh_token = jwt.encode(refresh_payload, PRIVATE_KEY, algorithm="RS256")

    return {"at": access_token, "rt": refresh_token, "jti": jti}

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        exp_time = payload.get("exp")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    return payload

