from flask import jsonify, session, send_file, render_template
import json
import pandas as pd


def sessionController(request):
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


def chartController(request, db):
    # comments = request.json['comments'].replace("&#39;", '"')
    user_uid = session["user"]["uid"]
    # video_date = int(request.json['video_info'])
    video_id = request.json["video_id"]
    typ = request.json["typ"]
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


def exportController(method):
    user_email = session["user"]["uid"]
    df = pd.read_csv(f"static/generated/{user_email}/dataset/data.csv")
    print(df)
    if df.empty:
        return (
            render_template(
                "message.html", error_message="No comments to export", status_code=400
            ),
            400,
        )
    if method == "csv":
        return send_file(
            f"static/generated/{user_email}/dataset/data.csv",
            mimetype="text/csv",
            as_attachment=True,
        )
    elif method == "xlsx":
        df.to_excel(f"static/generated/{user_email}/output/data.xlsx", index=False)
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
        return (
            render_template(
                "message.html", error_message="Unauthorized access", status_code=401
            ),
            401,
        )
