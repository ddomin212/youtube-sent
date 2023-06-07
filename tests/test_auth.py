from typing import Generator, Any
from flask import Flask
from unittest.mock import Mock, patch
from controllers.auth import registerController, profileController


def test_registerController(context: Generator[Flask, Any, None]):
    # Create a mock auth object
    auth = Mock()

    # Create a mock request object
    request = Mock()
    request.method = "POST"
    request.form.get.side_effect = lambda key: {
        "email": "test@example.com",
        "password": "password",
    }.get(key)

    # Call the registerController function with the mock objects
    response = registerController(auth, request)

    # Check the response
    assert response.status_code == 302
    assert response.location == "/login"


def test_profileController(
    context: Generator[Flask, Any, None], user_session: dict[str, dict[str, str]]
):
    # Create a mock auth object
    auth = Mock()

    # Create a mock request object
    request = Mock()
    request.method = "GET"
    request.args.get.side_effect = lambda key: {"user_id": "123"}.get(key)

    # Check the response
    with patch.dict("flask.session", user_session):
        response = profileController(auth, request)
        assert "Dan Dom" in response
