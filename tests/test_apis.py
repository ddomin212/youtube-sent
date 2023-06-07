from typing import Generator, Any
from flask import Flask
from unittest.mock import MagicMock, patch
from controllers.apis import sessionController, chartController, exportController


def test_sessionController(
    context: Generator[Flask, Any, None]
):  # the context is used througout any of the tests since it is a generator.
    request = MagicMock()
    request.json = {
        "name": "John",
        "password": "password123",
        "email": "john@example.com",
        "typ": "free",
        "tier": 1,
    }

    # Call the function and check the response
    response, status_code = sessionController(request)
    assert status_code == 200
    assert b"Session set successfully" in response.data


def test_chartController(
    context: Generator[Flask, Any, None],
    user_session: dict[str, dict[str, str]],
    history_entry: dict[str, Any],
):
    # Create a mock request object
    request = MagicMock()
    request.json = {"video_id": "123", "typ": "Week"}

    # Create a mock database object
    db = MagicMock()

    db.collection.return_value.where.return_value.where.return_value.stream.return_value = [
        MagicMock(to_dict=lambda: history_entry)
    ]

    # Call the function and check the response
    with patch.dict("flask.session", user_session):
        response = chartController(request, db)
        assert response is not None


def test_exportController(
    context: Generator[Flask, Any, None], user_session: dict[str, dict[str, str]]
):
    # Set up the mock request object

    with patch.dict("flask.session", user_session):
        # Call the function and check the response
        response = exportController("csv")
        assert response.status_code == 200
        assert response.mimetype == "text/csv"
