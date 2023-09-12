import json
import os
from typing import Any, Dict, List

import pandas as pd
from Flask import send_file, session

from connections.kaggle.get_sentiment import get_sentiment
from connections.kaggle.init_kaggle import init_kaggle
from connections.youtube.scrape_yt import get_comments
from utils.message import print_message


def set_user_session(request):
    name = request.json["name"]
    uid = request.json["password"]
    email = request.json["email"]
    typ = request.json["typ"]
    tier = request.json["tier"]
    session["user"] = {
        "uid": uid,
        "email": email,
        "typ": typ,
        "name": name if name else "User",
        "tier": tier,
        "verificationToken": "",
    }


def parse_json_cols(doc):
    json_columns = [
        "questions",
        "comments",
        "negatives",
        "weeks",
        "months",
        "years",
        "quest_counts",
        "pred_counts",
    ]
    for col in json_columns:
        doc[col] = json.loads(doc[col]) if doc[col] else []


def export_df(df, method, user_email):
    if method == "csv":
        return send_file(
            f"static/generated/{user_email}/dataset/data.csv",
            mimetype="text/csv",
            as_attachment=True,
        )
    elif method == "xlsx":
        df.to_excel(
            f"static/generated/{user_email}/output/data.xlsx", index=False
        )
        return send_file(
            f"static/generated/{user_email}/output/data.xlsx",
            mimetype="text/xlsx",
            as_attachment=True,
        )
    elif method == "json":
        df.to_json(f"static/generated/{user_email}/output/data.json")
        return send_file(
            f"static/generated/{user_email}/output/data.json",
            mimetype="application/json",
            as_attachment=True,
        )
    else:
        return print_message(400, "Invalid export method")


def check_first_time(user_email: str):
    """
    Checks if a user has used the application before by checking if a directory exists
    with the user's email address. If the directory does not exist, it creates it and initializes
    a Kaggle API client for the user.

    Args:
        user_email (str): The email address of the user.

    Returns:
        tuple: "no" if the directory already exists, "yes" if it was just created.
    """
    if os.path.exists(f"static/generated/{user_email}"):
        return "no"
    else:
        init_kaggle(user_email)
        return "yes"


def save_comments_to_csv(comments: List[Dict[str, Any]], user_email: str):
    """
    Saves a list of comments to a CSV file in the user's directory.

    Args:
        comments (dict): A list of comments to save.
        user_email (str): The email address of the user.

    Returns:
        tuple: A tuple containing the user's video history document and the video type.
    """
    comments_df = pd.DataFrame.from_dict(comments)
    comments_df.to_csv(
        f"static/generated/{user_email}/dataset/data.csv", index=False
    )
    return


def get_video_comments(request):
    full_url = request.form["url"]
    new_url = full_url.replace("watch?v=", "embed/")
    video_id = full_url.split("=")[1]
    comments, video_info = get_comments(video_id)
    return {
        "comments": comments,
        "video_info": video_info,
        "video_id": video_id,
    }


def get_sentiment_from_comments(comments):
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

    return {
        "quest_counts": quest_counts,
        "pred_counts": pred_counts,
        "negatives": negatives,
        "questions": questions,
        "user_email": user_email,
    }
