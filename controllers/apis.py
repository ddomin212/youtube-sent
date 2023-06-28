"""
Handles user sessions for the Flask application.

This module contains functions for setting user sessions based on a
JSON payload containing user information. 

Functions:
    sessionController: Sets the user's session based on a JSON payload containing user information.
    chartController: Retrieves the user's video data and returns a response containing 
                                                            the requested chart data.
    exportController: Exports the user's comments to the specified format and returns a response 
                                                                    containing the exported data.
"""
import json

import pandas as pd
from flask import Request, jsonify, render_template, send_file, session
from functions.firebase import get_user_videos
from google.cloud.firestore import Client
from utils.message import print_message


def sessionController(request: Request):
    """
    Given a Flask request object containing a JSON payload with user information,
    sets the user's session and returns a response indicating success.

    Args:
        request (flask.Request): The Flask request object containing the JSON payload.

    Returns:
        Tuple[Response, int]: A tuple containing a Flask response object and an
        HTTP status code.
    """
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
    print("Session set successfully")
    return jsonify({"message": "Session set successfully"}), 200


def chartController(request: Request, db: Client):
    """
    Given a Flask request object and a database object, retrieves the user's video
    data and returns a response containing the requested chart data.

    Args:
        request (flask.Request): The Flask request object.
        db (google.cloud.firestore.Client): The database object.

    Returns:
        Response: A Flask response object containing the requested chart data.
    """
    doc, typ = get_user_videos(session, request, db)
    if doc == None:
        return print_message(404, "No data found for this video")
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
        doc[col] = json.loads(doc[col])
    if typ == "Week":
        return jsonify({"data": doc["weeks"]})
    elif typ == "Month":
        return jsonify({"data": doc["months"]})
    else:
        return jsonify({"data": doc["years"]})


def exportController(method: str):
    """
    Given a string indicating the export method, exports the user's comments to the
    specified format and returns a response containing the exported data, so that the user
    can download it.

    Args:
        method (str): The export method to use.

    Returns:
        Union[Response, Tuple[str, int]]: A Flask response object containing the
        exported data, or a tuple containing an error message and an HTTP status code.
    """
    user_email = session["user"]["uid"]
    df = pd.read_csv(f"static/generated/{user_email}/dataset/data.csv")
    if df.empty:
        return print_message(404, "No comments found for this video")
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
