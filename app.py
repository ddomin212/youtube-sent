from flask import Flask, render_template, request, jsonify, session, redirect, url_for, g, send_file
from config.init_app import config_app
from firebase_admin import auth
from functions import *
from utils.login_req import login_required
from utils.npenc import NpEncoder
from controllers.auth import registerController, profileController
from controllers.payment import paymentController, successController
from controllers.main import indexController, dashController, searchController
from controllers.history import historyController, showController
from controllers.apis import chartController, exportController, sessionController
from functions.firebase import add_to_firebase
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()
db, stripe, url, admin_uid = config_app(app)

# ==============================
# APIs
# ==============================
@app.route('/api/set-session', methods=['POST'])
def set_session():
    return sessionController(request)


@app.route('/api/export/<method>', methods=['GET'])
@login_required
def export(method):
    return exportController(method)
    
@app.route('/api/bar-chart', methods=['POST'])
@login_required
def bar_chart():
    return chartController(request, db)
# ==============================    
# ROUTES
# ==============================    
@app.route('/')
def index():
    return indexController()

@app.route('/dashboard')
@login_required
def dashboard():
    return dashController()


@app.route('/history', methods=['GET'])
@login_required
def history():
    return historyController(db)

@app.route('/show/<video_id>', methods=['GET'])
@login_required
def show(video_id):
    return showController(db, video_id)


@app.route('/payment', methods=['GET'])
@login_required
def create_checkout_session():
    return paymentController(stripe, url)

@app.route('/search', methods=['POST'])
@login_required
def search():
    return searchController(request, db)
    

@app.route('/payment-success', methods=['GET'])
@login_required
def success_payment():
    return successController(auth, request)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/pricing', methods=['GET'])
@login_required
def pricing():
    return render_template('pricing.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return profileController(auth, request)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    return registerController(auth, request)
# ==============================    
# 404 ERROR
# ==============================    
@app.errorhandler(404)
def not_found(e):
    return render_template('message.html', error_message="Could not find the page you were looking for", status_code=404), 404
# ==============================
# RUN APP
# ==============================
if __name__ == '__main__':
    app.run(debug=True)
