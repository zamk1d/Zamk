from pydantic import ValidationError

from src.schemas.routes.auth.auth_schemas import LoginSchema, RegisterSchema
from src.schemas.routes.token.token_schemas import TokenResponseSchema, AccessTokenSchema
import pytest

from tests.conftest import valid_password


def test_login_schema_with_valid_data(valid_email, valid_password):
    user = LoginSchema(email=valid_email, password=valid_password)

    assert user.email == valid_email
    assert user.password == valid_password

def test_register_schema_with_valid_data(valid_email, valid_password, valid_code):
    user = RegisterSchema(email=valid_email, password=valid_password, code=valid_code)

    assert user.email == valid_email
    assert user.password == valid_password
    assert user.code == valid_code

@pytest.mark.parametrize("invalid_email", ["", "abc", "mail@com", "mail@.", 1, None, True])
def test_login_schema_with_invalid_emails_raise_error(invalid_email, valid_password):
    with pytest.raises(ValidationError):
        LoginSchema(email=invalid_email, password=valid_password)

@pytest.mark.parametrize("invalid_password", [1, None, True])
def test_login_schema_with_invalid_passwords_raise_error(invalid_password, valid_email):
    with pytest.raises(ValidationError):
        LoginSchema(email=valid_email, password=invalid_password)

@pytest.mark.parametrize("invalid_email", ["", "abc", "mail@com", "mail@.", 1, None, True])
def test_register_schema_with_invalid_email_raise_error(invalid_email, valid_password, valid_code):
    with pytest.raises(ValidationError):
        RegisterSchema(email=invalid_email, password=valid_password, code=valid_code)

@pytest.mark.parametrize("invalid_password", ["", "1234", 1, None, True, "12345678910111213141516171819202122232425262728293031323334353637"])
def test_register_schema_with_invalid_password_raise_error(valid_email, invalid_password, valid_code):
    with pytest.raises(ValidationError):
        RegisterSchema(email=valid_email, password=invalid_password, code=valid_code)

@pytest.mark.parametrize("invalid_code", [1, None, True])
def test_register_schema_with_invalid_code_raise_error(valid_email, valid_password, invalid_code):
    with pytest.raises(ValidationError):
        RegisterSchema(email=valid_email, password=valid_password, code=invalid_code)