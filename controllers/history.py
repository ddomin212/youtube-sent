import itertools
from flask import render_template, session
import json


def historyController(db):
    user_uid = session["user"]["uid"]
    history = db.collection("history").where("uid", "==", user_uid).stream()
    history = [doc.to_dict() for doc in history]
    json_columns = [
        "questions",
        "comments",
        "negatives",
        "weeks",
        "quest_counts",
        "pred_counts",
    ]
    for doc, col in itertools.product(history, json_columns):
        doc[col] = json.loads(doc[col])
    return render_template("history.html", history=history)


def showController(db, video_id):
    user_uid = session["user"]["uid"]
    new_url = f"https://www.youtube.com/embed/{video_id}"
    history = (
        db.collection("history")
        .where("uid", "==", user_uid)
        .where("video_id", "==", video_id)
        .stream()
    )
    doc = [doc.to_dict() for doc in history][0]
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
