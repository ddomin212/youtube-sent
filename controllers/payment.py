from flask import redirect, session, render_template


def paymentController(stripe, url):
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
    session.get("user")["verificationToken"] = payment_session.id
    print(payment_session.id)
    return redirect(payment_session.url)


def successController(auth, request):
    payment_session_id = request.args.get("session_id")
    print(session["user"])
    if payment_session_id != session["user"]["verificationToken"]:
        return (
            render_template(
                "message.html", error_message="Unauthorized access", status_code=401
            ),
            401,
        )
    try:
        user = auth.get_user_by_email(session.get("user")["email"])
        auth.set_custom_user_claims(user.uid, {"tier": "premium"})
        session["user"]["tier"] = "premium"
    except Exception as e:
        print(e)
    return (
        render_template(
            "message.html", error_message="Payment successful", status_code=""
        ),
        200,
    )
