"""
Initializes the Flask app with the necessary settings and services.

This module contains functions for configuring the Redis client and Flask app settings, 
as well as initializing the required services such as Firebase and Stripe. 
The `config_redis_session` function configures the Redis client and assigns 
it as a target for the Flask session object. The `config_app_settings` 
function configures the Flask app with the necessary settings and initializes 
the required services, including the Firestore client, Stripe API key, app URL, and admin UID.

Functions:
    config_redis_session: Configures the Redis client and assigns it as 
                                a target for the Flask session object.
    config_app_settings: Configures the Flask app with the necessary 
                    settings and initializes the required services.
    config_app: Initializes the Flask app with the necessary settings and services.
    config_firebase: Initializes the Firebase app and returns the Firestore client.
"""
import os
import firebase_admin
from firebase_admin import credentials, firestore
from redis import Redis
from flask_session import Session
import stripe

def config_redis_session(app):
    """
    Configures the Redis client and assings it as a target for the Flask session object.

    Returns:
        Redis: The Redis client.
    """
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = Redis(host=os.getenv('REDIS_HOST'),
                                        port=os.getenv('REDIS_PORT'),
                                        password=os.getenv('REDIS_PASSWORD'))
    Session(app)

def config_app_settings(app):
    """
    Configures the Flask app with the necessary settings and initializes the required services.

    Args:
        app: The Flask app instance.

    Returns:
        A tuple containing the Firestore client, Stripe API key, app URL, and admin UID.
    """

    url = os.getenv('APP_URL')
    app.secret_key = os.getenv('PAGE_SECRET')
    stripe.api_key = os.getenv("STRIPE_API_KEY")
    admin_uid = os.getenv('ADMIN_UID')
    return url, admin_uid

def config_firebase():
    """
    Configures the Firebase app with the necessary settings and initializes the required services.

    Args:
        app: The Flask app instance.

    Returns:
        A tuple containing the Firestore client, Stripe API key, app URL, and admin UID.
    """

    cred = credentials.Certificate("./config/app.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    return db

def config_app(app):
    """
    Configures the Flask app with the necessary settings and initializes the required services.

    Args:
        app: The Flask app instance.

    Returns:
        A tuple containing the Firestore client, Stripe API key, app URL, and admin UID.
    """

    url, admin_uid = config_app_settings(app)
    db = config_firebase()
    config_redis_session(app)
    return db, url, admin_uid
