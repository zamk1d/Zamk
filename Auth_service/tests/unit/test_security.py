import pytest

from src.services.security.hash_password import verify_password, hash_password
from src.services.security.token_signature import create_jwt, verify_token

from fastapi import HTTPException

def test_password_hashing():
    password = "password"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)

def test_jwt_signature():
    payload = {"sub": "1234"}
    result = create_jwt(payload)
    at, rt, jti = result.get("at"), result.get("rt"), result.get("jti")

    verified_at_payload = verify_token(at)
    verified_rt_payload = verify_token(rt)

    assert set(verified_at_payload.keys()) == {"sub", "exp", "type"}
    assert set(verified_rt_payload.keys()) == {"sub", "exp", "type", "jti"}

    assert verified_at_payload["sub"] == payload["sub"]

def test_expired_token():
    payload = {"sub": "1234"}
    result = create_jwt(payload, access_exp_minutes=0, refresh_exp_days=0)

    with pytest.raises(HTTPException) as exc_info:
        verify_token(result["at"])
    assert exc_info.value.status_code == 401

    with pytest.raises(HTTPException) as exc_info:
        verify_token(result["rt"])
    assert exc_info.value.status_code == 401