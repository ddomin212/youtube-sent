from flask import session, render_template, g
import os
import pandas as pd
from functions import init_kaggle, get_comments, get_sentiment
from functions.firebase import upload_firebase


def indexController():
    if not session.get("user"):
        return render_template("index.html")
    else:
        return render_template("dash.html", first=True)


def dashController():
    return render_template("dash.html", first=True)


def searchController(request, db):
    full_url = request.form["url"]
    new_url = full_url.replace("watch?v=", "embed/")
    video_id = full_url.split("=")[1]
    user_email = session["user"]["uid"]
    first_time = "no" if os.path.isdir(f"static/generated/{user_email}") else "yes"
    if first_time == "yes":
        init_kaggle(user_email)
    comments, video_info = get_comments(video_id)

    df = pd.DataFrame.from_dict(comments)
    df.to_csv(f"static/generated/{user_email}/dataset/data.csv", index=False)
    quest_counts, pred_counts, negatives, questions = get_sentiment(
        comments, user_email, first_time
    )
    df = pd.DataFrame.from_dict(comments)
    df.to_csv(f"static/generated/{user_email}/dataset/data.csv", index=False)

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
