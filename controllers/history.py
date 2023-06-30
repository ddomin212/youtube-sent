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
from google.cloud.firestore import Client
from connections.firebase import firebase_query
from utils.message import print_message
from utils.controllers import parse_json_cols

def historyController(db: Client):
    """
    Given a database object, retrieves the user's history data and returns a
    response containing the history page template with the retrieved data.

    Args:
        db (google.cloud.firestore.Client): The database object
                                    to use for history data retrieval.

    Returns:
        Response: A Flask response object containing the history page template
        with the retrieved data.
    """
    user_uid = session["user"]["uid"]
    with firebase_query(db, "history", [("uid", "==", user_uid)]) as data:
        if data is None:
            return print_message(
                404, "Found no history data. Please try again later."
            )
        for doc in data:
            parse_json_cols(doc)
        return render_template("history.html", history=data)


def showController(db: Client, video_id: str):
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
    with firebase_query(
        db, "history", [("uid", "==", user_uid), ("video_id", "==", video_id)]
    ) as data:
        if data is None:
            return print_message(404, "Found no history data. Please try again later.")
        doc = data[0]
        parse_json_cols(doc)
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
