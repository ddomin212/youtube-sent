from flask import session, render_template, g
import json
import os
import pandas as pd
from functions import init_kaggle, get_comments, get_sentiment, get_weeks
from utils.npenc import NpEncoder
from functions.firebase import add_to_firebase

def indexController():
    if not session.get('user'):
        return render_template('index.html')
    else:
        return render_template('dash.html', first=True)
    
def dashController():
    print(session['user'])
    return render_template('dash.html', first=True)

def searchController(request, db):
    full_url = request.form.get('url')
    new_url = full_url.replace("watch?v=", "embed/")
    video_id = full_url.split('=')[1]
    user_email = session['user']['uid']
    first_time = "no" if os.path.isdir(
        f"static/generated/{user_email}") else "yes"
    if first_time == "yes":
        init_kaggle(user_email)
    """comments = pd.read_csv(
        open(f"static/generated/{user_email}/dataset/data.csv", encoding="utf8")).fillna(0)
    print(comments.info())
    comments = comments.to_dict('records')"""
    comments, video_info = get_comments(video_id)
    df = pd.DataFrame.from_dict(comments)
    df.to_csv(f"static/generated/{user_email}/dataset/data.csv", index=False)
    quest_counts, pred_counts, negatives, questions = get_sentiment(
        comments, user_email, first_time)
    df = pd.DataFrame.from_dict(comments)
    df.to_csv(f"static/generated/{user_email}/dataset/data.csv", index=False)
    # video_info = ["some", "cunt", 1679094012]
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
        "pred_counts": json.dumps(pred_counts, cls=NpEncoder)
    }
    add_to_firebase(data, video_id, user_email, db)
    g.loading_complete = True
    return render_template('dash.html', questions=questions, max_diff=max_diff, quest_counts=list(quest_counts.values()),
                           weeks=weeks, negatives=negatives, pred_counts=list(pred_counts.values()), video_id=video_id,
                           comments=comments, items=3, carousels=4, user_email=user_email, video_info=video_info, full_url=new_url)
