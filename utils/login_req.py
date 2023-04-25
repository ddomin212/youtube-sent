from flask import session, render_template
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            render_template(
                'message.html', error_message="Unauthorized - not logged in", status_code=401), 401
        return f(*args, **kwargs)
    return decorated_function