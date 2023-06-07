"""
This module contains functions for interacting with Firebase and retrieving user video history.
"""

import json
from typing import Any, Dict, List
from flask import Request
from flask_session import Session
from google.cloud.firestore import Client
from utils.npenc import NpEncoder
from .youtube.scrape_helpers import get_weeks


def get_user_videos(session: Dict[str, Dict[str, Any]], request: Request, db: Client):
    """
    Retrieves the user's video history for a given video ID and type.

    Args:
        session (dict): The user's session data.
        request (flask.Request): The HTTP request object.
        db (google.cloud.firestore.client.Client): The Firestore client instance.

    Returns:
        tuple: A tuple containing the user's video history document and the video type.
    """
    user_uid = session["user"]["uid"]
    video_id = request.json["video_id"]
    typ = request.json["typ"]
    history = (
        db.collection("history")
        .where("uid", "==", user_uid)
        .where("video_id", "==", video_id)
        .stream()
    )
    doc = [doc.to_dict() for doc in history][0]
    return doc, typ


def add_to_firebase(data: Dict[str, Any], video_id: str, user_uid: str, db: Client):
    """
    Adds a video document to Firestore for a given video ID and user ID.

    Args:
        data (dict): The video history data to add.
        video_id (str): The ID of the video being watched.
        user_uid (str): The ID of the user requesting the addition.
        db (google.cloud.firestore.client.Client): The Firestore client instance.
    """
    users_ref = db.collection("history")
    doc_ref = users_ref.document(f"{str(video_id)}|{str(user_uid)}")
    print(data)
    doc_ref.set(data)


def upload_firebase(
    video_info: str,
    user_email: str,
    video_id: str,
    db: Client,
    pred_counts: Dict[str, int],
    quest_counts: Dict[str, int],
    questions: List[Dict[str, Any]],
    negatives: List[Dict[str, Any]],
    comments: List[Dict[str, Any]],
):
    """
    Uploads video data to Firestore for a given video ID and user email.

    Args:
        video_info (dict): The video information to upload.
        user_email (str): The email of the user watching the video.
        video_id (str): The ID of the video being watched.
        db (google.cloud.firestore.client.Client): The Firestore client instance.
        pred_counts (dict): The prediction counts for the video.
        quest_counts (dict): The question counts for the video.
        questions (list): The list of questions asked during the video.
    """
    weeks, max_diff = get_weeks(comments, video_info[2], 7)
    months, _ = get_weeks(comments, video_info[2], 30)
    years, _ = get_weeks(comments, video_info[2], 365)
    comments = sorted(comments, key=lambda x: x["comment_like_count"])[:15]
    questions = sorted(questions, key=lambda x: x["comment_like_count"])[:15]
    negatives = sorted(negatives, key=lambda x: x["comment_like_count"])[:15]
    data = {
        "uid": user_email,
        "video_id": video_id,
        "questions": json.dumps(questions, cls=NpEncoder),
        "comments": json.dumps(comments, cls=NpEncoder),
        "negatives": json.dumps(negatives, cls=NpEncoder),
        "weeks": json.dumps(weeks, cls=NpEncoder),
        "months": json.dumps(months, cls=NpEncoder),
        "years": json.dumps(years, cls=NpEncoder),
        "max_diff": max_diff,
        "video_info": video_info,
        "quest_counts": json.dumps(quest_counts, cls=NpEncoder),
        "pred_counts": json.dumps(pred_counts, cls=NpEncoder),
    }
    add_to_firebase(data, video_id, user_email, db)
    return max_diff, weeks
