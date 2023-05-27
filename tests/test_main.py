from unittest.mock import patch, MagicMock
from controllers.main import indexController, searchController, dashController
import pandas as pd
import pytest

def test_index_controller(context, user_session):
    with patch.dict('flask.session', {'user': None}):
        response = indexController()
        assert "CommentWiz" in response
    with patch.dict('flask.session', user_session):
        response = indexController()
        print(response)
        assert "Dashboard" in response

def test_dash_controller(context, user_session):
    with patch.dict('flask.session', user_session):
        response = dashController()
        assert "Dashboard" in response

@pytest.mark.skip(reason="Taking too long to run")
def test_search_controller(context, user_session):
    request = MagicMock()
    request.form = {"url": "https://www.youtube.com/watch?v=7d9Ao2DMvtA"}
    db = MagicMock()
    with patch("pandas.DataFrame.to_csv") as mock_save:
        with patch("controllers.main.init_kaggle") as mock_init_kaggle:
            with patch("controllers.main.get_comments") as mock_get_comments:
                with patch.dict("flask.session", user_session):
                    mock_save.return_value = None
                    mock_get_comments.return_value = (pd.read_csv("static/generated/user123/dataset/data.csv").to_dict(orient='records'), 
                                                        ("Testing", "Tester", 1685154212))
                    response = searchController(request, db)
                    assert "Peter MacDonald" in response
                    assert "Alex Hormozi" in response
