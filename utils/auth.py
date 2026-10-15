from functools import wraps
from urllib.parse import urlparse

from flask import flash, g, redirect, request, session, url_for

from models.user import get_user_by_id


def get_current_user():
    """Return the logged-in user from the database, or None."""
    user_id = session.get("user_id")
    if user_id is None:
        return None
    return get_user_by_id(user_id)


def login_required(view):
    """Redirect unauthenticated visitors to the login page."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user = get_current_user()
        if user is None:
            session.clear()
            flash("Please log in to continue.", "info")
            return redirect(url_for("auth.login", next=request.path))
        g.user = user
        return view(*args, **kwargs)

    return wrapped_view


def is_safe_redirect_target(target):
    """Allow only relative paths on this site, to prevent open redirects."""
    if not target or "\\" in target:
        return False
    parsed = urlparse(target)
    return not parsed.scheme and not parsed.netloc and target.startswith("/") and not target.startswith("//")
