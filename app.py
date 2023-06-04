import stripe
from firebase_admin import auth
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
)
from config.init_app import config_app
from utils.login_req import login_required
from controllers.auth import registerController, profileController
from controllers.payment import paymentController, successController
from controllers.main import indexController, dashController, searchController
from controllers.history import historyController, showController
from controllers.apis import chartController, exportController, sessionController



app = Flask(__name__)
load_dotenv()
db, url, admin_uid = config_app(app)


# ==============================
# APIs
# ==============================

@app.route("/api/set-session", methods=["POST"])
def set_session():
    """
    Sets the session data for the user.

    Returns:
        The response from the sessionController function.
    """
    return sessionController(request)


@app.route("/api/export/<method>", methods=["GET"])
@login_required
def export(method):
    """
    Exports data for the user in the specified format.

    Args:
        method: The export method to use.

    Returns:
        The response from the exportController function.
    """
    return exportController(method)


@app.route("/api/bar-chart", methods=["POST"])
@login_required
def bar_chart():
    """
    Generates a bar chart for the user's video history.

    Returns:
        The response from the chartController function.
    """
    return chartController(request, db)


# ==============================
# ROUTES
# ==============================

@app.route("/")
def index():
    """
    Renders the index page.

    Returns:
        The response from the indexController function.
    """
    return indexController()


@app.route("/dashboard")
@login_required
def dashboard():
    """
    Renders the dashboard page.

    Returns:
        The response from the dashController function.
    """
    return dashController()


@app.route("/history", methods=["GET"])
@login_required
def history():
    """
    Renders the user's video history page.

    Returns:
        The response from the historyController function.
    """
    return historyController(db)


@app.route("/show/<video_id>", methods=["GET"])
@login_required
def show(video_id):
    """
    Renders the video dashboard page for the specified video from a firebase document.

    Args:
        video_id: The ID of the video to display.

    Returns:
        The response from the showController function.
    """
    return showController(db, video_id)


@app.route("/payment", methods=["GET"])
@login_required
def create_checkout_session():
    """
    Creates a checkout session for the user.

    Returns:
        The response from the paymentController function.
    """
    return paymentController(stripe, url)


@app.route("/search", methods=["POST"])
@login_required
def search():
    """
    Renders the video dashboard page for the specified video.

    Returns:
        The response from the searchController function.
    """
    return searchController(request, db)


@app.route("/payment-success", methods=["GET"])
@login_required
def success_payment():
    """
    Renders the payment success page.

    Returns:
        The response from the successController function.
    """
    return successController(auth, request)


@app.route("/login", methods=["GET"])
def login():
    """
    Renders the login page.

    Returns:
        The rendered login template.
    """
    return render_template("login.html")


@app.route("/pricing", methods=["GET"])
@login_required
def pricing():
    """
    Renders the pricing page.

    Returns:
        The rendered pricing template.
    """
    return render_template("pricing.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
    Renders the user's profile page (only for Email/Password users).

    Returns:
        The response from the profileController function.
    """
    return profileController(auth, request)


@app.route("/logout")
def logout():
    """
    Logs the user out of the application.

    Returns:
        A redirect to the index page.
    """
    session.clear()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Renders the registration page.

    Returns:
        The response from the registerController function.
    """
    return registerController(auth, request)


# ==============================
# 404 ERROR
# ==============================

@app.errorhandler(404)
def not_found(e):
    """
    Renders the 404 error page.

    Returns:
        The rendered message template.
    """
    return (
        render_template(
            "message.html",
            error_message="Could not find the page you were looking for",
            status_code=404,
        ),
        404,
    )


# ==============================
# RUN APP
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
