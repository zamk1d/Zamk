from fastapi import HTTPException

import pytest
from unittest.mock import AsyncMock, patch
from src.services.auth import login, register, TokenResponseSchema

@pytest.mark.asyncio
@patch("src.services.auth.get_user", new_callable=AsyncMock)
@patch("src.services.auth.create_jwt")
@patch("src.services.auth.set_jti", new_callable=AsyncMock)
async def test_login_with_valid_credentials_returns_tokens(mock_set_jti, mock_create_jwt, mock_get_user, valid_email, valid_password):

    mock_get_user.return_value = "user-uuid-123"
    mock_create_jwt.return_value = {"at": "access-token", "rt": "refresh-token", "jti": "jti-123"}

    result = await login(email=valid_email, password=valid_password, db=None)

    assert isinstance(result, TokenResponseSchema)
    assert result.access_token == "access-token"
    assert result.refresh_token == "refresh-token"

    mock_set_jti.assert_awaited_once_with(uuid="user-uuid-123", jti="jti-123", db=None)
    mock_get_user.assert_awaited_once()
    mock_create_jwt.assert_called_once()

@pytest.mark.asyncio
@patch("src.services.auth.check_code", new_callable=AsyncMock)
@patch("src.services.auth.redis.delete", new_callable=AsyncMock)
@patch("src.services.auth.create_user", new_callable=AsyncMock)
@patch("src.services.auth.create_jwt")
@patch("src.services.auth.set_jti", new_callable=AsyncMock)
async def test_register_with_valid_credentials_and_email_code_returns_tokens(
        mock_set_jti, mock_create_jwt, mock_create_user, mock_delete, mock_check_code, valid_email, valid_password, valid_code):

    mock_check_code.return_value = True
    mock_create_user.return_value = "user-uuid-123"
    mock_create_jwt.return_value = {"at": "access-token", "rt": "refresh-token", "jti": "jti-123"}

    result = await register(email=valid_email, password=valid_password, code=valid_code, db=None)

    assert isinstance(result, TokenResponseSchema)
    assert result.access_token == "access-token"
    assert result.refresh_token == "refresh-token"

    mock_set_jti.assert_awaited_once_with(uuid="user-uuid-123", jti="jti-123", db=None)
    mock_check_code.assert_awaited_once()
    mock_create_user.assert_awaited_once()
    mock_create_jwt.assert_called_once()
    mock_delete.assert_awaited_once_with(f"verify_code: {valid_email}")

@pytest.mark.asyncio
@patch("src.services.auth.check_code", new_callable=AsyncMock)
async def test_register_with_valid_credentials_and_invalid_email_code_raises_http_exception_403(mock_check_code, valid_email, valid_password, valid_code):

    mock_check_code.return_value = False
    with pytest.raises(HTTPException) as exc_info:
        await register(email=valid_email, password=valid_password, code=valid_code, db=None)

    assert "Invalid code" in str(exc_info.value)
    mock_check_code.assert_awaited_once()