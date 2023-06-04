"""
Handles the user's video history for the Flask application.

This module contains functions for retrieving the user's video history data 
from the database and rendering the history page template with the retrieved data.

Functions:
    historyController: Given a database object, retrieves the user's history data and 
                                        returns a response containing the history page 
                                                    template with the retrieved data.
"""

import json
from flask import render_template, session

def historyController(db):
    """
    Given a database object, retrieves the user's history data and returns a
    response containing the history page template with the retrieved data.

    Args:
        db (google.cloud.firestore.client.Client): The database object 
                                    to use for history data retrieval.

    Returns:
        Response: A Flask response object containing the history page template
        with the retrieved data.
    """
    user_uid = session["user"]["uid"]
    history = [doc.to_dict() for doc in (db.collection("history")
                                         .where("uid", "==", user_uid)
                                         .stream())]
    json_columns = [
        "questions",
        "comments",
        "negatives",
        "weeks",
        "quest_counts",
        "pred_counts",
    ]
    history = [{col: json.loads(doc.get(col, "[]"))
                if col in json_columns else doc.get(col)
                for col in doc.keys()}
                for doc in history]
    return render_template("history.html", history=history)


def showController(db, video_id):
    """
    Given a database object and a video ID, retrieves the user's history data for
    the specified video and returns a response containing the show page template
    with the retrieved data.

    Args:
        db (google.cloud.firestore.client.Client): The database object to use for 
                                                            history data retrieval.
        video_id (str): The ID of the video to retrieve history data for.

    Returns:
        Response: A Flask response object containing the show page template with
        the retrieved data.
    """
    user_uid = session["user"]["uid"]
    new_url = f"https://www.youtube.com/embed/{video_id}"
    doc = [doc.to_dict() for doc in  (db.collection("history")
                                    .where("uid", "==", user_uid)
                                    .where("video_id", "==", video_id)
                                    .stream())][0]
    json_columns = [
        "questions",
        "comments",
        "negatives",
        "weeks",
        "quest_counts",
        "pred_counts",
    ]
    for col in json_columns:
        doc[col] = json.loads(doc[col])
    return render_template(
        "dash.html",
        questions=doc["questions"],
        max_diff=doc["max_diff"],
        quest_counts=list(doc["quest_counts"].values()),
        weeks=doc["weeks"],
        negatives=doc["negatives"],
        pred_counts=list(doc["pred_counts"].values()),
        video_id=doc["video_id"],
        comments=doc["comments"],
        items=3,
        carousels=4,
        user_email=user_uid,
        video_info=doc["video_info"],
        full_url=new_url,
    )
