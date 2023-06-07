"""
Main module for the Flask application.

This module contains the main controllers for the Flask application, 
including the index, dashboard, and search controllers. 

Functions:
    indexController: Renders the index or dashboard template depending on whether the user is logged in.
    dashController: Renders the dashboard template with the first-time user flag set to True.
    searchController: Given a Flask request object and a database object, 
                    retrieves the comments and sentiment analysis data for a
                    YouTube video specified in the request.
"""
from flask import session, render_template, g, Request
from google.cloud.firestore import Client
from functions import get_comments, get_sentiment
from functions.firebase import upload_firebase
from functions.data import check_first_time, save_comments_to_csv


def indexController():
    """
    If the user is not logged in, renders the index template. Otherwise, renders
    the dashboard template with the first-time user flag set to True.

    Returns:
        str: The rendered index or dashboard template.
    """
    if not session.get("user"):
        return render_template("index.html")
    else:
        return render_template("dash.html", first=True)


def dashController():
    """
    Renders the dashboard template with the first-time user flag set to True.

    Returns:
        str: The rendered dashboard template.
    """
    return render_template("dash.html", first=True)


def searchController(request: Request, db: Client):
    """
    Given a Flask request object and a database object, retrieves the comments and
    sentiment analysis data for a YouTube video specified in the request
    and renders the search template with the retrieved data.

    Args:
        request (flask.Request): The Flask request object containing the video URL.
        db (google.cloud.firestore.client.Client): The database object to use for user data storage.

    Returns:
        str: The rendered search template with the retrieved data.
    """
    full_url = request.form["url"]
    new_url = full_url.replace("watch?v=", "embed/")
    video_id = full_url.split("=")[1]
    user_email = session["user"]["uid"]
    first_time = check_first_time(user_email)
    comments, video_info = get_comments(video_id)

    save_comments_to_csv(comments, user_email)

    quest_counts, pred_counts, negatives, questions = get_sentiment(
        comments, user_email, first_time
    )

    save_comments_to_csv(comments, user_email)

    max_diff, weeks = upload_firebase(
        video_info,
        user_email,
        video_id,
        db,
        pred_counts,
        quest_counts,
        questions,
        negatives,
        comments,
    )
    g.loading_complete = True

    return render_template(
        "dash.html",
        questions=questions,
        max_diff=max_diff,
        quest_counts=list(quest_counts.values()),
        weeks=weeks,
        negatives=negatives,
        pred_counts=list(pred_counts.values()),
        video_id=video_id,
        comments=comments,
        items=3,
        carousels=4,
        user_email=user_email,
        video_info=video_info,
        full_url=new_url,
    )
