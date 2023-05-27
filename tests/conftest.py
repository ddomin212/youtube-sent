from app import app
import pytest


@pytest.fixture()
def context():
    with app.test_request_context():
        yield app

@pytest.fixture()
def user_session():
    return {'user': {'uid': 'user123', 'email': 'dan.dom@gmail.com',
                    'name': 'Dan Dom', 'verificationToken': 'session123', 'tier': 'free'}}