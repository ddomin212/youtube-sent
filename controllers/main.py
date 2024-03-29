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
from flask import Request, g, render_template, session
from google.cloud.firestore import Client

from connections.firebase import upload_firebase
from connections.kaggle.get_sentiment import get_sentiment
from connections.youtube.scrape_yt import get_comments
from utils.controllers import check_first_time, save_comments_to_csv
from utils.message import print_message


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
    # get video comments
    full_url = request.form["url"]
    new_url = full_url.replace("watch?v=", "embed/")
    video_id = full_url.split("=")[1]
    comments, video_info = get_comments(video_id)

    # get the sentiment from kaggle
    user_email = session["user"]["uid"]
    first_time = check_first_time(user_email)

    if comments is None:
        return print_message(
            404, "Found no comments. Ensure the video has comments enabled."
        )

    save_comments_to_csv(comments, user_email)

    quest_counts, pred_counts, negatives, questions = get_sentiment(
        comments, user_email, first_time
    )

    if quest_counts is None:
        return print_message(
            500, "Could not fetch sentiment data. Please try again later."
        )

    save_comments_to_csv(comments, user_email)

    # upload to firebase
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

    # render the template
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
