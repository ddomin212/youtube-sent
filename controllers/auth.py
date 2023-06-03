from flask import render_template, redirect, session


def registerController(auth, request):
    """
    Given an auth object and a Flask request object containing user registration
    information, creates a new user and redirects to the login page if successful,
    or returns an error message if unsuccessful.

    Args:
        auth (Any): The auth object to use for user creation.
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
    except Exception:
        return (
            render_template(
                "message.html", error_message="User creation failed", status_code=400
            ),
            400
        )


def profileController(auth, request):
    """
    Given an auth object and a Flask request object containing user profile information,
    updates the user's profile and returns a response containing the updated profile
    information.

    Args:
        auth (Any): The auth object to use for user profile updates.
        request (flask.Request): The Flask request object containing the user profile information.

    Returns:
        Response: A Flask response object containing the updated user profile information.
    """
    if request.method == "POST":
        name = request.form.get("fullname")
        email = request.form.get("email")
        try:
            user = auth.get_user_by_email(session.get("user")["email"])
            auth.update_user(user.uid, display_name=name, email=email)
        except Exception as e:
            print(e)
        session["user"]["email"] = email
        session["user"]["name"] = name
    return render_template("profile.html", user=session["user"])
