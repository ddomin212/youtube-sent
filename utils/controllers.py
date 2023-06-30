import json
import os

import pandas as pd
from Flask import session, send_file

from utils.message import print_message
from typing import Any, Dict, List
from connections.kaggle.init_kaggle import init_kaggle

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