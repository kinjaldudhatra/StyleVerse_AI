import secrets

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from models.user import EmailAlreadyRegisteredError, create_user, get_user_by_email
from utils.auth import is_safe_redirect_target
from utils.csrf import is_csrf_token_valid
from utils.validators import GENDER_CHOICES, validate_login, validate_registration

auth_bp = Blueprint("auth", __name__)

INVALID_CREDENTIALS_MESSAGE = "Invalid email or password."
CSRF_ERROR_MESSAGE = "Your session expired. Please try again."
REGISTRATION_FIELDS = ["name", "email", "password", "confirm_password", "gender"]

# Used to keep response timing similar when the submitted email is not registered.
PLACEHOLDER_HASH = generate_password_hash(secrets.token_hex(16))


def render_register(status=200, form_values=None, error_fields=()):
    """Render the registration page with the previously entered safe values."""
    return render_template(
        "register.html",
        form_values=form_values or {},
        error_fields=error_fields,
        genders=GENDER_CHOICES,
    ), status


def render_login(status=200, email="", error_fields=()):
    """Render the login page, keeping the safe redirect target if present."""
    next_url = request.values.get("next", "")
    if not is_safe_redirect_target(next_url):
        next_url = ""
    return render_template(
        "login.html", email=email, error_fields=error_fields, next_url=next_url
    ), status


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Display the registration form and create a new user account."""
    if session.get("user_id"):
        return redirect(url_for("main.dashboard"))
    if request.method == "GET":
        return render_register()

    if not is_csrf_token_valid():
        flash(CSRF_ERROR_MESSAGE, "error")
        return render_register(400)

    cleaned, errors = validate_registration(request.form)
    if errors:
        for message in errors.values():
            flash(message, "error")
        error_fields = REGISTRATION_FIELDS if "required" in errors else errors.keys()
        return render_register(400, cleaned, error_fields=error_fields)

    password_hash = generate_password_hash(request.form["password"])
    try:
        create_user(cleaned["name"], cleaned["email"], password_hash, cleaned["gender"])
    except EmailAlreadyRegisteredError:
        flash("This email is already registered. Please log in instead.", "error")
        return render_register(409, cleaned, error_fields=["email"])

    flash("Account created successfully. Please log in.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Display the login form and start a session for valid credentials."""
    if session.get("user_id"):
        return redirect(url_for("main.dashboard"))
    if request.method == "GET":
        return render_login()

    if not is_csrf_token_valid():
        flash(CSRF_ERROR_MESSAGE, "error")
        return render_login(400)

    email, error_message = validate_login(request.form)
    if error_message:
        flash(error_message, "error")
        return render_login(400, email, error_fields=["email", "password"])

    user = get_user_by_email(email)
    # Verify the submitted password against the securely stored password hash.
    stored_hash = user["password_hash"] if user else PLACEHOLDER_HASH
    password_is_valid = check_password_hash(stored_hash, request.form["password"])
    if user is None or not password_is_valid:
        flash(INVALID_CREDENTIALS_MESSAGE, "error")
        return render_login(401, email, error_fields=["email", "password"])

    # Start a fresh session to avoid reusing any session data from before login.
    session.clear()
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    flash("Logged in successfully.", "success")

    next_url = request.form.get("next", "")
    if is_safe_redirect_target(next_url):
        return redirect(next_url)
    return redirect(url_for("main.dashboard"))


@auth_bp.route("/logout")
def logout():
    """End the current session and return to the home page."""
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("main.index"))
