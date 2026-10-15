from flask import Blueprint, g, render_template
from models.database import fetch_one
from utils.auth import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Render the StyleVerse AI landing page."""
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    # Keep your existing code above this point.

    tryon_count_row = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM tryon_history
        WHERE user_id = ?
        """,
        (g.user["id"],),
    )

    tryon_count = tryon_count_row["total"]

    return render_template(
        "dashboard.html",
        user=g.user,
        tryon_count=tryon_count,
    )


@main_bp.route("/virtual-try-on")
@login_required
def virtual_try_on():
    """Render the Virtual Try-On page."""
    return render_template("virtual_try_on.html")
