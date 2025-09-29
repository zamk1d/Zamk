import pytest

@pytest.fixture
def valid_email():
    return "valid@gmail.com"

@pytest.fixture
def valid_password():
    return "valid_password"

@pytest.fixture
def valid_code():
    return "000000"

@pytest.fixture
def valid_payload():
    return {"sub": "1234"}