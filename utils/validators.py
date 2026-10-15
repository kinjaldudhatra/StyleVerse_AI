import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
GENDER_CHOICES = {
    "female": "Female",
    "male": "Male",
    "prefer_not_to_say": "Prefer not to say",
}
NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 60
EMAIL_MAX_LENGTH = 254
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128

REQUIRED_FIELDS_MESSAGE = "Please complete all required fields."


def normalize_email(email):
    """Return the email in the consistent format used for storage and lookup."""
    return email.strip().lower()


def is_valid_email(email):
    """Check that the email has a basic valid format and a reasonable length."""
    return len(email) <= EMAIL_MAX_LENGTH and bool(EMAIL_PATTERN.match(email))


def validate_password_strength(password):
    """Return an error message if the password breaks the policy, otherwise None."""
    if len(password) < PASSWORD_MIN_LENGTH:
        return f"Password must be at least {PASSWORD_MIN_LENGTH} characters long."
    if len(password) > PASSWORD_MAX_LENGTH:
        return f"Password must be at most {PASSWORD_MAX_LENGTH} characters long."
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return "Password must contain at least one letter and one number."
    return None


def validate_registration(form):
    """Validate the registration form.

    Returns a tuple of cleaned values and a dictionary of field errors.
    """
    cleaned = {
        "name": " ".join(form.get("name", "").split()),
        "email": normalize_email(form.get("email", "")),
        "gender": form.get("gender", ""),
    }
    password = form.get("password", "")
    confirm_password = form.get("confirm_password", "")
    errors = {}

    required_values = [cleaned["name"], cleaned["email"], password, confirm_password, cleaned["gender"]]
    if not all(required_values):
        errors["required"] = REQUIRED_FIELDS_MESSAGE
        return cleaned, errors

    if not NAME_MIN_LENGTH <= len(cleaned["name"]) <= NAME_MAX_LENGTH:
        errors["name"] = (
            f"Name must be between {NAME_MIN_LENGTH} and {NAME_MAX_LENGTH} characters."
        )
    if not is_valid_email(cleaned["email"]):
        errors["email"] = "Please enter a valid email address."
    password_error = validate_password_strength(password)
    if password_error:
        errors["password"] = password_error
    elif password != confirm_password:
        errors["confirm_password"] = "Passwords do not match."
    if cleaned["gender"] not in GENDER_CHOICES:
        errors["gender"] = "Please select a valid gender option."

    return cleaned, errors


def validate_login(form):
    """Validate the login form.

    Returns a tuple of the normalized email and an error message, or None.
    """
    email = normalize_email(form.get("email", ""))
    password = form.get("password", "")

    if not email or not password:
        return email, REQUIRED_FIELDS_MESSAGE
    if not is_valid_email(email):
        return email, "Please enter a valid email address."
    return email, None
