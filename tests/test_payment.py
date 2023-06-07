from unittest.mock import patch, MagicMock
from typing import Generator, Any
from flask import Flask
from firebase_admin import auth
from pytest import MonkeyPatch
from controllers.payment import paymentController, successController


def test_paymentController(
    context: Generator[Flask, Any, None], user_session: dict[str, dict[str, str]]
):
    mock_session = MagicMock()
    mock_session.create.return_value = MagicMock(
        url="https://example.com/checkout", id="session123"
    )
    mock_checkout = MagicMock()
    mock_checkout.Session.return_value = mock_session
    with patch("stripe.checkout", mock_checkout):
        with patch.dict("flask.session", user_session):
            response = paymentController("https://example.com")
            assert response.status_code == 302


def test_successController(
    context: Generator[Flask, Any, None],
    user_session: dict[str, dict[str, str]],
    monkeypatch: Generator[MonkeyPatch, None, None],
):
    def mock_get_user_by_email():
        return {"uid": "user123"}

    def mock_set_custom_user_claims():
        pass

    monkeypatch.setattr(auth, "get_user_by_email", mock_get_user_by_email)
    monkeypatch.setattr(auth, "set_custom_user_claims", mock_set_custom_user_claims)

    with patch.dict("flask.session", user_session):
        mock_request = MagicMock()
        mock_request.args = {"session_id": "session123"}
        response, status_code = successController(auth, mock_request)
        print(response)
        assert status_code == 200
        assert "Payment successful" in response
