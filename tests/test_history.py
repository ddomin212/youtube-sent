from unittest.mock import Mock, patch
from controllers.history import historyController, showController
import json

def test_historyController(context, user_session, history_entry):
    # Create a mock session object
    session = {"user": {"uid": "user123"}}

    # Create a mock database object
    db = Mock()
    db.collection.return_value.where.return_value.stream.return_value = [
        Mock(to_dict=lambda: history_entry)
    ]

    # Call the historyController function with the mock objects
    with patch.dict('flask.session', user_session):
        response = historyController(db)

    # Check the response
    print(response)
    assert 'Test Name of Video' in response
    
def test_showController(context, user_session, history_entry):
    # Create a mock session object
    session = {"user": {"uid": "user123"}}

    # Create a mock database object
    db = Mock()
    db.collection.return_value.where.return_value.where.return_value.stream.return_value = [
        Mock(to_dict=lambda: history_entry)
    ]

    # Call the showController function with the mock objects
    with patch.dict('flask.session', user_session):
        response = showController(db, '123')

    # Check the response
    print(response)
    assert 'Test Name of Video' in response
    assert 'by Test' in response
    assert 'sounds pretty toxic to me' in response