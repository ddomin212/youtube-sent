from flask import session, render_template
from functools import wraps

def login_required(f):
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
        if not session.get('user'):
            render_template(
                'message.html', error_message="Unauthorized - not logged in", status_code=401), 401
        return f(*args, **kwargs)
    return decorated_function