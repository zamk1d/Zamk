import pytest

from src.config.custom_exceptions import MissingSubClaimError
from src.services.security.hash_password import verify_password, hash_password
from src.services.security.token_signature import create_jwt, verify_token

from fastapi import HTTPException

def test_password_hashing_with_string_data_returns_hash():
    password = "password"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)

def test_jwt_signature_with_correct_arguments_returns_tokens_and_jti(valid_payload):
    result = create_jwt(valid_payload)
    at, rt, jti = result.get("at"), result.get("rt"), result.get("jti")

    verified_at_payload = verify_token(at)
    verified_rt_payload = verify_token(rt)

    assert set(verified_at_payload.keys()) == {"sub", "exp", "type"}
    assert set(verified_rt_payload.keys()) == {"sub", "exp", "type", "jti"}

    assert verified_at_payload["sub"] == valid_payload["sub"]

def test_jwt_signature_with_empty_payload_raises_missing_sub_claim_error():
    with pytest.raises(MissingSubClaimError) as exc_info:
        create_jwt({})

    assert "'sub' claim is required in payload" in str(exc_info.value)

def test_jwt_signature_with_0_time_raises_http_exception_401(valid_payload):
    result = create_jwt(valid_payload, access_exp_minutes=0, refresh_exp_days=0)

    with pytest.raises(HTTPException) as exc_info:
        verify_token(result["at"])
    assert exc_info.value.status_code == 401

    with pytest.raises(HTTPException) as exc_info:
        verify_token(result["rt"])
    assert exc_info.value.status_code == 401