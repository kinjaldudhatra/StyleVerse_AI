import hmac
import secrets

from flask import request, session


def generate_csrf_token():
    """Return the CSRF token for the current session, creating it when missing."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def is_csrf_token_valid():
    """Check the submitted form token against the token stored in the session."""
    expected_token = session.get("csrf_token", "")
    submitted_token = request.form.get("csrf_token", "")
    return bool(expected_token) and hmac.compare_digest(expected_token, submitted_token)
