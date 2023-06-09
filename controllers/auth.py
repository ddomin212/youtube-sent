"""
Handles user authentication for the Flask application.

This module contains functions for registering new users and logging in existing users.

Functions:
    registerController: Creates a new user and redirects to the login 
                        page if successful, or returns an error message if unsuccessful.
    loginController: Logs the user in if successful, or returns an error message if unsuccessful.
"""

from firebase_admin import auth
from flask import Request, redirect, render_template, session
from google.cloud.exceptions import GoogleCloudError
from utils.message import print_message


def registerController(auth: auth, request: Request):
    """
    Given an auth object and a Flask request object containing user registration
    information, creates a new user and redirects to the login page if successful,
    or returns an error message if unsuccessful.

    Args:
        auth (firebase_admin.auth): The auth object to use for user creation.
        request (flask.Request): The Flask request object containing the user registration
        information.

    Returns:
        Union[Response, Tuple[Response, int]]: A Flask response object if successful,
        or a tuple containing a Flask response object and an HTTP status code if
        unsuccessful.
    """
    if request.method != "POST":
        return render_template("register.html")
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        auth.create_user(email=email, password=password)
        return redirect("/login")
    except GoogleCloudError:
        return print_message(500, "Error creating user")


def profileController(auth: auth, request: Request):
    """
    Given an auth object and a Flask request object containing user profile information,
    updates the user's profile and returns a response containing the updated profile
    information.

    Args:
        auth (firebase_admin.auth): The auth object to use for user profile updates.
        request (flask.Request): The Flask request object containing the user profile information.

    Returns:
        Response: A Flask response object containing the updated user profile information.
    """
    if request.method == "POST":
        name = request.form.get("fullname")
        email = request.form.get("email")
        try:
            user = auth.get_user_by_email(session["user"]["email"])
            auth.update_user(user.uid, display_name=name, email=email)
        except GoogleCloudError:
            return print_message(500, "Error updating user")
        session["user"]["email"] = email
        session["user"]["name"] = name
    return render_template("profile.html", user=session["user"])
