from flask import render_template


def print_message(status_code, message):
    return (
        render_template(
            "message.html",
            error_message=message,
            status_code=status_code,
        ),
        status_code,
    )
