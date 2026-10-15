from pathlib import Path

from flask import (
    abort,
    current_app,
    flash,
    redirect,
    url_for,
)
from models.database import fetch_all, get_connection
from utils.csrf import is_csrf_token_valid
from flask import Blueprint, render_template, session
from utils.auth import login_required

tryon_history_bp = Blueprint(
    "tryon_history",
    __name__,
    url_prefix="/try-on-history",
)


@tryon_history_bp.route("/")
@login_required
def index():
    """Show only the logged-in user's previous try-on results."""
    user_id = session.get("user_id")

    history = fetch_all(
        """
        SELECT id, outfit_name, result_image, created_at
        FROM tryon_history
        WHERE user_id = ?
        ORDER BY created_at DESC, id DESC
        """,
        (user_id,),
    )

    return render_template(
        "tryon_history.html",
        history=history,
    )

@tryon_history_bp.post("/<int:history_id>/delete")
@login_required
def delete(history_id):
    """Delete only the logged-in user's saved try-on result."""

    if not is_csrf_token_valid():
        abort(400, description="Invalid security token. Refresh and try again.")

    user_id = session.get("user_id")

    # Find a history record belonging to this user only.
    with get_connection() as connection:
        item = connection.execute(
            """
            SELECT id, result_image
            FROM tryon_history
            WHERE id = ? AND user_id = ?
            """,
            (history_id, user_id),
        ).fetchone()

        if item is None:
            abort(404)

        # Accept only filenames inside the try-on history folder.
        image_name = Path(item["result_image"]).name
        expected_relative_path = (
            f"images/tryon_history/{image_name}"
        )

        if (
            not image_name
            or item["result_image"] != expected_relative_path
        ):
            abort(400, description="Invalid history image path.")

        connection.execute(
            """
            DELETE FROM tryon_history
            WHERE id = ? AND user_id = ?
            """,
            (history_id, user_id),
        )

    # Remove the corresponding image, without touching outfit images.
    image_path = (
        Path(current_app.static_folder)
        / "images"
        / "tryon_history"
        / image_name
    )

    try:
        image_path.unlink(missing_ok=True)
    except OSError:
        current_app.logger.exception(
            "Could not remove try-on history image."
        )

    flash("Try-on result deleted successfully.", "success")
    return redirect(url_for("tryon_history.index"))
