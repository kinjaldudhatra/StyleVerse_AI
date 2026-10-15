
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models.user import get_user_profile, update_user_profile
from utils.auth import login_required
from utils.csrf import is_csrf_token_valid

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")

GENDER_CHOICES = {"Female", "Male"}
SKIN_TONES = {"Fair", "Light", "Medium", "Olive", "Deep"}
FACE_SHAPES = {"Oval", "Round", "Square", "Heart", "Diamond", "Oblong"}
CLOTHING_SIZES = {"XS", "S", "M", "L", "XL", "XXL"}
STYLE_PREFERENCES = {
    "Casual", "Formal", "Traditional", "Western", "Streetwear", "Minimalist"
}
FAVORITE_COLORS = {
    "Black", "White", "Red", "Blue", "Pink", "Purple",
    "Green", "Yellow", "Brown", "Beige", "Other"
}
OCCASIONS = {
    "Daily Wear", "College", "Office", "Party", "Wedding", "Festive"
}


@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session.get("user_id")
    user = get_user_profile(user_id)

    if user is None:
        flash("Your account could not be found. Please log in again.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        if not is_csrf_token_valid():
            flash("Your session expired. Please try again.", "error")
            return redirect(url_for("profile.index"))

        name = request.form.get("name", "").strip()
        gender = request.form.get("gender", "").strip()
        skin_tone = request.form.get("skin_tone", "").strip()
        face_shape = request.form.get("face_shape", "").strip()
        clothing_size = request.form.get("clothing_size", "").strip()
        style_preference = request.form.get("style_preference", "").strip()
        favorite_color = request.form.get("favorite_color", "").strip()
        preferred_occasion = request.form.get("preferred_occasion", "").strip()

        if not name or len(name) > 100:
            flash("Enter a name between 1 and 100 characters.", "error")
        elif gender not in GENDER_CHOICES:
            flash("Please select a valid gender.", "error")
        elif skin_tone and skin_tone not in SKIN_TONES:
            flash("Please select a valid skin tone.", "error")
        elif face_shape and face_shape not in FACE_SHAPES:
            flash("Please select a valid face shape.", "error")
        elif clothing_size and clothing_size not in CLOTHING_SIZES:
            flash("Please select a valid clothing size.", "error")
        elif style_preference and style_preference not in STYLE_PREFERENCES:
            flash("Please select a valid style preference.", "error")
        elif favorite_color and favorite_color not in FAVORITE_COLORS:
            flash("Please select a valid favorite color.", "error")
        elif preferred_occasion and preferred_occasion not in OCCASIONS:
            flash("Please select a valid occasion.", "error")
        else:
            update_user_profile(
                user_id,
                name,
                gender,
                skin_tone,
                face_shape,
                clothing_size,
                style_preference,
                favorite_color,
                preferred_occasion,
            )
            session["user_name"] = name
            flash("Your profile has been updated successfully!", "success")
            return redirect(url_for("profile.index"))

        # Keep the user's submitted values visible if validation fails.
        user = {
            **dict(user),
            "name": name,
            "gender": gender,
            "skin_tone": skin_tone,
            "face_shape": face_shape,
            "clothing_size": clothing_size,
            "style_preference": style_preference,
            "favorite_color": favorite_color,
            "preferred_occasion": preferred_occasion,
        }

    return render_template("profile.html", user=user)
