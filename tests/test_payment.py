import stripe
from controllers.payment import paymentController, successController
from unittest.mock import patch, MagicMock
from firebase_admin import auth

def test_paymentController(context, user_session):
    mock_session = MagicMock()
    mock_session.create.return_value = MagicMock(url="https://example.com/checkout", id="session123")
    mock_checkout = MagicMock()
    mock_checkout.Session.return_value = mock_session
    with patch("stripe.checkout", mock_checkout):
        with patch.dict("flask.session", user_session):
            response = paymentController(stripe, "https://example.com")
            assert response.status_code == 302

def test_successController(context, monkeypatch, user_session):
    def mock_get_user_by_email(email):
        return {"uid": "user123"}

    def mock_set_custom_user_claims(uid, claims):
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
        