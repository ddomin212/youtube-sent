import os
import firebase_admin
from firebase_admin import credentials, firestore
from redis import Redis
from flask_session import Session
import stripe

def config_app(app):
# configure the app
    url = os.getenv('APP_URL')
    app.secret_key = os.getenv('PAGE_SECRET')

    # configure the session to use redis
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = Redis(host=os.getenv('REDIS_HOST'),
                                        port=os.getenv('REDIS_PORT'), password=os.getenv('REDIS_PASSWORD'))
    Session(app)
    # initialize Firebase SDK

    cred = credentials.Certificate("./config/app.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    stripe.api_key = os.getenv("STRIPE_API_KEY")
    # Define a decorator to check if the user is logged in
    admin_uid = os.getenv('ADMIN_UID')

    return db, stripe, url, admin_uid