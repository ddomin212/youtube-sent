"""
Handles user authentication for Flask routes.

This module contains a decorator 
function for checking if the user is logged in.

Functions:
    login_required: A decorator function that checks if the user is logged in.
"""
from typing import Callable
from functools import wraps
from flask import session, render_template


def login_required(f: Callable):
    """
    A decorator function that checks if the user is logged in before allowing access
    to a Flask route. If the user is not logged in, returns a 401 Unauthorized error.

    Args:
        f (function): The Flask route function to decorate.

    Returns:
        function: The decorated Flask route function.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            return (
                render_template(
                    "message.html",
                    error_message="Unauthorized - not logged in",
                    status_code=401,
                ),
                401,
            )
        return f(*args, **kwargs)

    return decorated_function
