from flask import Flask, render_template, request, jsonify, session, redirect, url_for, g, send_file
import firebase_admin
from firebase_admin import credentials, auth, firestore
from firebase_cfg import firebase_config
from functools import wraps
from redis import Redis
from flask_session import Session
import stripe
from comments_scrape import get_comments, get_weeks
from kaggle_helpers import get_sentiment, init_kaggle
import pickle
import pandas as pd
import numpy as np
import os
import json
import re

app = Flask(__name__)
url = "http://localhost:3000"
app.secret_key = "testing key"
# configure the session to use redis
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='redis-10870.c55.eu-central-1-1.ec2.cloud.redislabs.com',
                                    port=10870, password='wMRKxucbAnyQhuGkdVC5f6SPtGv8EjbT')
Session(app)
# initialize Firebase SDK
cred = credentials.Certificate("./app.json")
firebase_admin.initialize_app(cred)
stripe.api_key = "sk_test_51MH5EwIkzhBkf9zaD02EAQytK9dGQoV90wVunTVCotcjOTe5KE8PROAnohNpzzqVudhwx26hVM7rUXrydyvDQIZk00j8me5aMt"
# Define a decorator to check if the user is logged in
admin_uid = "qiA05vUZnGOJJegRN5nZvI27h7a2"
db = firestore.client()
# define helper functions


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super(NpEncoder, self).default(obj)


def add_to_firebase(data, video_id, user_uid):
    # Get a reference to the document collection
    users_ref = db.collection('history')
    # Create a document
    doc_ref = users_ref.document(str(video_id) + "|" + str(user_uid))
    print(data)
    doc_ref.set(data)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            render_template(
                'message.html', error_message="Unauthorized - not logged in", status_code=401), 401
        return f(*args, **kwargs)
    return decorated_function

# Define APIs


@app.route('/api/set-session', methods=['POST'])
def set_session():
    name = request.json['name']
    uid = request.json['password']
    email = request.json['email']
    type = request.json['type']
    tier = request.json['tier']
    session['user'] = {'uid': uid, 'email': email,
                       'type': type, 'name': name if name else 'User', 'tier': tier, 'verificationToken': ''}
    print("Session set successfully")
    return jsonify({'message': 'Session set successfully'}), 200


@app.route('/api/export/<method>', methods=['GET'])
@login_required
def export(method):
    print(method)
    user_email = session["user"]["uid"]
    df = pd.read_csv(f"static/generated/{user_email}/dataset/data.csv")
    if df.empty:
        return render_template(
            'message.html', error_message="No comments to export", status_code=400), 400
    if method == "csv":
        return send_file(f"static/generated/{user_email}/dataset/data.csv", mimetype='text/csv', as_attachment=True)
    elif method == "xlsx":
        df.to_excel(
            f"static/generated/{user_email}/output/data.xlsx", index=False)
        return send_file(f"static/generated/{user_email}/output/data.xlsx", mimetype='text/xlsx', as_attachment=True)
    elif method == "json":
        df.to_json(f"static/generated/{user_email}/output/data.json")
        return send_file(f"static/generated/{user_email}/output/data.json", mimetype='application/json', as_attachment=True)
    else:
        return render_template(
            'message.html', error_message="Unauthorized access", status_code=401), 401


@app.route('/api/bar-chart', methods=['POST'])
@login_required
def bar_chart():
    # comments = request.json['comments'].replace("&#39;", '"')
    user_uid = session["user"]["uid"]
    # video_date = int(request.json['video_info'])
    video_id = request.json['video_id']
    type = request.json['type']
    history = db.collection('history').where(
        'uid', '==', user_uid).where('video_id', '==', video_id).stream()
    doc = [doc.to_dict() for doc in history][0]
    json_columns = ["questions",
                    "comments",
                    "negatives",
                    "weeks",
                    "months",
                    "years",
                    "quest_counts",
                    "pred_counts"]
    for col in json_columns:
        doc[col] = json.loads(doc[col])
    if type == "Week":
        return jsonify({"data": doc["weeks"]})
    elif type == "Month":
        return jsonify({"data": doc["months"]})
    else:
        return jsonify({"data": doc["years"]})
# Define the routes for each page


@app.route('/')
def index():
    if not session.get('user'):
        return render_template('index.html')
    else:
        return render_template('dash.html', first=True)


@app.route('/dashboard')
@login_required
def dashboard():
    print(session['user'])
    return render_template('dash.html', first=True)


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        try:
            auth.generate_password_reset_link(email)
            return render_template('message.html', error_message="Password reset link sent to your email", status_code=200), 200
        except Exception as e:
            return render_template('message.html', error_message=e, status_code=404), 404
    else:
        return render_template('forgot-password.html')


@app.route('/show/<video_id>', methods=['GET'])
@login_required
def show(video_id):
    user_uid = session['user']['uid']
    new_url = "https://www.youtube.com/embed/" + video_id
    history = db.collection('history').where(
        'uid', '==', user_uid).where('video_id', '==', video_id).stream()
    doc = [doc.to_dict() for doc in history][0]
    json_columns = ["questions",
                    "comments",
                    "negatives",
                    "weeks",
                    "quest_counts",
                    "pred_counts"]
    for col in json_columns:
        doc[col] = json.loads(doc[col])
    return render_template('dash.html', questions=doc["questions"], max_diff=doc["max_diff"], quest_counts=list(doc["quest_counts"].values()),
                           weeks=doc["weeks"], negatives=doc["negatives"], pred_counts=list(
                               doc["pred_counts"].values()),
                           video_id=doc["video_id"], comments=doc["comments"], items=3, carousels=4, user_email=user_uid, video_info=doc["video_info"], full_url=new_url)


@app.route('/history', methods=['GET'])
@login_required
def history():
    user_uid = session['user']['uid']
    history = db.collection('history').where(
        'uid', '==', user_uid).stream()
    history = [doc.to_dict() for doc in history]
    json_columns = ["questions",
                    "comments",
                    "negatives",
                    "weeks",
                    "quest_counts",
                    "pred_counts"]
    for doc in history:
        for col in json_columns:
            doc[col] = json.loads(doc[col])
    return render_template('history.html', history=history)


@app.route('/search', methods=['POST'])
@login_required
def search():
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
    add_to_firebase(data, video_id, user_email)
    g.loading_complete = True
    return render_template('dash.html', questions=questions, max_diff=max_diff, quest_counts=list(quest_counts.values()),
                           weeks=weeks, negatives=negatives, pred_counts=list(pred_counts.values()), video_id=video_id,
                           comments=comments, items=3, carousels=4, user_email=user_email, video_info=video_info, full_url=new_url)


@app.route('/payment', methods=['GET'])
@login_required
def create_checkout_session():
    payment_session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        line_items=[
            {
                "price": "price_1MZWerIkzhBkf9zaHbc0qq2q",
                "quantity": 1,
            },
        ],
        success_url=f'{url}/payment-success?session_id={"{CHECKOUT_SESSION_ID}"}',
        cancel_url=f'{url}/cancel',
    )
    session.get('user')['verificationToken'] = payment_session.id
    print(session['user'])
    return redirect(payment_session.url)


@app.route('/payment-success', methods=['GET'])
@login_required
def success_payment():
    payment_session_id = request.args.get('session_id')
    print(session['user'])
    if payment_session_id == session['user']['verificationToken']:
        try:
            user = auth.get_user_by_email(session.get('user')['email'])
            auth.set_custom_user_claims(user.uid, {"tier": "premium"})
            session['user']['tier'] = "premium"
        except Exception as e:
            print(e)
        return render_template(
            'message.html', error_message="Payment successful", status_code=""), 200
    else:
        return render_template(
            'message.html', error_message="Unauthorized access", status_code=401), 401


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/pricing', methods=['GET', 'POST'])
@login_required
def pricing():
    return render_template('pricing.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # get user input from request body
        name = request.form.get('fullname')
        email = request.form.get('email')
        user = auth.get_user_by_email(session.get('user')['email'])
        try:
            # update user account with email and password
            auth.update_user(user.uid, display_name=name, email=email)
        except Exception as e:
            print(e)
        session['user']['email'] = email
        session['user']['name'] = name
        return render_template('profile.html', user=session['user'])
    else:
        return render_template('profile.html', user=session['user'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        # register route for email/password authentication
        # get user input from request body
        email = request.form.get('email')
        password = request.form.get('password')

        # create user account with email and password
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            return redirect('/login')
        except:
            return render_template('message.html', error_message="User creation failed", status_code=400), 400
    else:
        return render_template("register.html")

# Handle 404 errors


@app.errorhandler(404)
def not_found(e):
    return render_template('message.html', error_message="Could not find the page you were looking for", status_code=404), 404


if __name__ == '__main__':
    app.run(debug=True)
