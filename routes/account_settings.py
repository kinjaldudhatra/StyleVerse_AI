
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models.user import change_user_password
from utils.auth import login_required
from utils.csrf import is_csrf_token_valid

account_settings_bp = Blueprint(
    "account_settings",
    __name__,
    url_prefix="/account-settings",
)


@account_settings_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        if not is_csrf_token_valid():
            flash("Your session expired. Please try again.", "error")
            return redirect(url_for("account_settings.index"))

        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not current_password or not new_password or not confirm_password:
            flash("Please fill in all password fields.", "error")
        elif len(new_password) < 8:
            flash("Your new password must be at least 8 characters.", "error")
        elif len(new_password) > 128:
            flash("Your new password is too long.", "error")
        elif new_password != confirm_password:
            flash("The new passwords do not match.", "error")
        elif new_password == current_password:
            flash("Choose a password different from your current one.", "error")
        else:
            success, message = change_user_password(
                session["user_id"],
                current_password,
                new_password,
            )
            flash(message, "success" if success else "error")

            if success:
                return redirect(url_for("account_settings.index"))

    return render_template("account_settings.html")
