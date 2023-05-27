from unittest.mock import Mock, patch
from controllers.history import historyController, showController
import json

def test_historyController(context, user_session):
    # Create a mock session object
    session = {"user": {"uid": "user123"}}

    # Create a mock database object
    db = Mock()
    db.collection.return_value.where.return_value.stream.return_value = [
        Mock(to_dict=lambda: {
            "uid": "user123",
            "video_id": "123",
            "video_info": ["Test Name of Video", "Test", "01-01-2010"],
            "questions": "[]",
            "comments": "[]",
            "negatives": "[]",
            "weeks": "[]",
            "quest_counts": "[]",
            "pred_counts": "[]"
        })
    ]

    # Call the historyController function with the mock objects
    with patch.dict('flask.session', user_session):
        response = historyController(db)

    # Check the response
    print(response)
    assert 'Test Name of Video' in response
    
def test_showController(context, user_session):
    # Create a mock session object
    session = {"user": {"uid": "user123"}}

    # Create a mock database object
    db = Mock()
    db.collection.return_value.where.return_value.where.return_value.stream.return_value = [
        Mock(to_dict=lambda: {
            "uid": "user123",
            "video_id": "123",
            "video_info": ["Test Name of Video", "Test", "01-01-2010"],
            "questions": json.dumps([{"comment_text": "sounds pretty toxic to me", "comment_author": "Hurstiisio", "comment_author_url": "http://www.youtube.com/channel/UCRGVtPkgO26VUyCYmVVChwQ", "comment_author_image": "https://yt3.ggpht.com/uC1GO3uEhApyD0iwQ77Zbb1sSx2sG3cGofTsGDEH3PjxPrHc9CuXkKOyiylx2FDJgF6gAIeC2w=s48-c-k-c0x00ffffff-no-rj", "comment_published_at": "2023-03-26T12:09:27Z", "comment_published_at_unix": 1679832567, "comment_like_count": 0, "comment_id": "UgySnyUb8oMANeV9ez14AaABAg.9DKF882fcTM9nibSklfPq7", "comment_parent_id": "UgySnyUb8oMANeV9ez14AaABAg", "comment_sentiment": 0}]),
            "max_diff": "13",
            "comments": json.dumps([{"comment_text": "sounds pretty toxic to me", "comment_author": "Hurstiisio", "comment_author_url": "http://www.youtube.com/channel/UCRGVtPkgO26VUyCYmVVChwQ", "comment_author_image": "https://yt3.ggpht.com/uC1GO3uEhApyD0iwQ77Zbb1sSx2sG3cGofTsGDEH3PjxPrHc9CuXkKOyiylx2FDJgF6gAIeC2w=s48-c-k-c0x00ffffff-no-rj", "comment_published_at": "2023-03-26T12:09:27Z", "comment_published_at_unix": 1679832567, "comment_like_count": 0, "comment_id": "UgySnyUb8oMANeV9ez14AaABAg.9DKF882fcTM9nibSklfPq7", "comment_parent_id": "UgySnyUb8oMANeV9ez14AaABAg", "comment_sentiment": 0}]),
            "negatives": json.dumps([{"comment_text": "sounds pretty toxic to me", "comment_author": "Hurstiisio", "comment_author_url": "http://www.youtube.com/channel/UCRGVtPkgO26VUyCYmVVChwQ", "comment_author_image": "https://yt3.ggpht.com/uC1GO3uEhApyD0iwQ77Zbb1sSx2sG3cGofTsGDEH3PjxPrHc9CuXkKOyiylx2FDJgF6gAIeC2w=s48-c-k-c0x00ffffff-no-rj", "comment_published_at": "2023-03-26T12:09:27Z", "comment_published_at_unix": 1679832567, "comment_like_count": 0, "comment_id": "UgySnyUb8oMANeV9ez14AaABAg.9DKF882fcTM9nibSklfPq7", "comment_parent_id": "UgySnyUb8oMANeV9ez14AaABAg", "comment_sentiment": 0}]),
            "weeks": json.dumps({"0": [858, 4], "1": [246, 3], "2": [203, 2], "3": [2628, 14]}),
            "months": json.dumps({"0": [858, 4], "1": [246, 3], "2": [203, 2], "3": [2628, 14]}),
            "years": json.dumps({"0": [858, 4], "1": [246, 3], "2": [203, 2], "3": [2628, 14]}),
            "quest_counts": json.dumps({"true": 1, "false": 1}),
            "pred_counts": json.dumps({"true": 1, "false": 1})
        })
    ]

    # Call the showController function with the mock objects
    with patch.dict('flask.session', user_session):
        response = showController(db, '123')

    # Check the response
    print(response)
    assert 'Test Name of Video' in response
    assert 'by Test' in response
    assert 'sounds pretty toxic to me' in response