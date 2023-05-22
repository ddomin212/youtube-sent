from .youtube.scrape_helpers import get_weeks
from utils.npenc import NpEncoder
import json


def add_to_firebase(data, video_id, user_uid, db):
    # Get a reference to the document collection
    users_ref = db.collection("history")
    # Create a document
    doc_ref = users_ref.document(f"{str(video_id)}|{str(user_uid)}")
    print(data)
    doc_ref.set(data)


def upload_firebase(
    video_info,
    user_email,
    video_id,
    db,
    pred_counts,
    quest_counts,
    questions,
    negatives,
    comments,
):
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
        "pred_counts": json.dumps(pred_counts, cls=NpEncoder),
    }
    add_to_firebase(data, video_id, user_email, db)
    return max_diff, weeks
