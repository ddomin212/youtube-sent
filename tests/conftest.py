from app import app
import pytest
import json

@pytest.fixture()
def context():
    with app.test_request_context():
        yield app

@pytest.fixture()
def user_session():
    return {'user': {'uid': 'user123', 'email': 'dan.dom@gmail.com',
                    'name': 'Dan Dom', 'verificationToken': 'session123', 'tier': 'free'}}


@pytest.fixture()
def history_entry():
    return {
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
        }