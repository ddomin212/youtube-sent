"""
Handles payment processing for the Flask application.

This module contains a function for creating a new payment session for a subscription and redirecting the user to the Stripe checkout page.

Functions:
    paymentController: Given a Stripe object and a URL, creates a new payment session 
                        for a subscription and redirects the user to the Stripe checkout page.
"""
import stripe
from firebase_admin import auth
from flask import Request, redirect, render_template, session
from utils.message import print_message


def paymentController(url: str):
    """
    Given a Stripe object and a URL, creates a new payment session for a subscription
    and redirects the user to the Stripe checkout page.

    Args:
        stripe (stripe): The Stripe object to use for payment session creation.
        url (str): The URL to redirect the user to after payment.

    Returns:
        Response: A Flask response object redirecting the user to the Stripe checkout page.
    """
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
        cancel_url=f"{url}/cancel",
    )
    if payment_session is None:
        return print_message(500, "Error creating Stripe payment session")
    session.get("user")["verificationToken"] = payment_session.id
    print(payment_session.id)
    return redirect(payment_session.url)


def successController(fbauth: auth, request: Request):
    """
    Given an auth object and a Flask request object containing a payment session ID,
    verifies the payment session ID and updates the user's custom claims if successful,
    or returns an error message if unsuccessful.

    Args:
        auth (google.cloud.auth): The auth object to use for user custom claims updates.
        request (flask.Request): The Flask request object containing the payment session ID.

    Returns:
        Tuple[str, int]: A tuple containing a rendered success message and an HTTP status code.
    """
    payment_session_id = request.args.get("session_id")
    print(session["user"])
    if payment_session_id != session["user"]["verificationToken"]:
        return print_message(500, "Error verifying payment")
    try:
        user = fbauth.get_user_by_email(session.get("user")["email"])
        fbauth.set_custom_user_claims(user.uid, {"tier": "premium"})
        session["user"]["tier"] = "premium"
    except Exception as e:
        print(e)
    return print_message(200, "Payment successful")
