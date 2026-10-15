import os
import uuid
from pathlib import Path

from flask import session
import io
import requests

from flask import (
    Blueprint,
    current_app,
    jsonify,
    request,
    send_file,
    url_for,
)
from PIL import Image, UnidentifiedImageError

from models.database import get_connection
from utils.auth import login_required
from utils.csrf import is_csrf_token_valid


virtual_tryon_bp = Blueprint(
    "virtual_tryon",
    __name__,
    url_prefix="/virtual-try-on",
)


ALLOWED_CATEGORIES = {
    # Full outfits
    "dress": "one-pieces",
    "gown": "one-pieces",
    "anarkali": "one-pieces",
    "lehenga": "one-pieces",
    "sharara": "one-pieces",
    "saree": "one-pieces",
    "kurta set": "one-pieces",
    "co-ord set": "one-pieces",
    "western": "one-pieces",
    "kurti": "one-pieces",

    # Tops
    "top": "tops",
    "shirt": "tops",
    "t-shirt": "tops",
    "blouse": "tops",

    # Bottoms
    "jeans": "bottoms",
    "trousers": "bottoms",
    "pants": "bottoms",
    "skirt": "bottoms",
    "shorts": "bottoms",
}


ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}


@virtual_tryon_bp.post("/generate")
@login_required
def generate_tryon():
    if not is_csrf_token_valid():
        return jsonify({"error": "Invalid security token. Refresh the page and try again."}), 400

    person_file = request.files.get("person_image")
    outfit_id = request.form.get("outfit_id", type=int)
    garment_photo_type = request.form.get(
        "garment_photo_type", "flat-lay"
    )

    if not person_file or not person_file.filename:
        return jsonify({"error": "Please upload or capture your photo."}), 400

    if not outfit_id:
        return jsonify({"error": "Please select an outfit."}), 400

    if garment_photo_type not in {"model", "flat-lay"}:
        return jsonify({"error": "Invalid outfit photo type."}), 400

    try:
        person_bytes = person_file.read(10 * 1024 * 1024 + 1)

        if not person_bytes or len(person_bytes) > 10 * 1024 * 1024:
            return jsonify({"error": "Your photo must be 10 MB or smaller."}), 400

        with Image.open(io.BytesIO(person_bytes)) as image:
            if image.format not in ALLOWED_IMAGE_FORMATS:
                return jsonify({"error": "Use a JPEG, PNG, or WEBP photo."}), 400
            image.verify()

    except (UnidentifiedImageError, OSError):
        return jsonify({"error": "The uploaded photo is not a valid image."}), 400

    with get_connection() as connection:
        outfit = connection.execute(
            "SELECT id, name, category, image FROM outfits WHERE id = ?",
            (outfit_id,),
        ).fetchone()

    if not outfit:
        return jsonify({"error": "The selected outfit was not found."}), 404

    category = ALLOWED_CATEGORIES.get(
        str(outfit["category"]).strip().lower()
    )

    if not category:
        return jsonify({
            "error": (
                f"AI try-on is not configured for the "
                f"'{outfit['category']}' category yet."
            )
        }), 400

    image_name = outfit["image"]

    # Only allow a filename, not a user-supplied path.
    if not image_name or image_name != image_name.split("/")[-1] or "\\" in image_name:
        return jsonify({"error": "The outfit image filename is invalid."}), 400

    garment_path = (
        current_app.static_folder
        and __import__("pathlib").Path(current_app.static_folder)
        / "images"
        / "outfits"
        / image_name
    )

    if not garment_path or not garment_path.is_file():
        return jsonify({
            "error": f"Outfit image '{image_name}' was not found."
        }), 404

    try:
        with open(garment_path, "rb") as garment_file:
            garment_bytes = garment_file.read(10 * 1024 * 1024 + 1)

        if len(garment_bytes) > 10 * 1024 * 1024:
            return jsonify({"error": "The outfit image is too large."}), 400

        with Image.open(io.BytesIO(garment_bytes)) as image:
            if image.format not in ALLOWED_IMAGE_FORMATS:
                return jsonify({"error": "The outfit image format is unsupported."}), 400
            image.verify()

    except (UnidentifiedImageError, OSError):
        return jsonify({"error": "The outfit image is invalid or unreadable."}), 400

    try:
        response = requests.post(
            f"{current_app.config['VTON_SERVICE_URL'].rstrip('/')}/try-on",
            files={
                "person_image": (
                    person_file.filename or "person.jpg",
                    person_bytes,
                    "application/octet-stream",
                ),
                "garment_image": (
                    image_name,
                    garment_bytes,
                    "application/octet-stream",
                ),
            },
            data={
                "category": category,
                "garment_photo_type": garment_photo_type,
            },
            timeout=(10, 300),
        )

        if not response.ok:
            try:
                error_data = response.json()
                message = error_data.get("error", "AI try-on failed.")
            except ValueError:
                message = "The AI service returned an unexpected error."

            return jsonify({"error": message}), response.status_code

        result = response.content

        
        # Check that the AI response is a valid image.
        with Image.open(io.BytesIO(result)) as image:
            image.verify()

        # Save the generated result.
        history_folder = (
            Path(current_app.static_folder)
            / "images"
            / "tryon_history"
        )
        history_folder.mkdir(parents=True, exist_ok=True)

        user_id = session.get("user_id")
        unique_filename = f"user_{user_id}_{uuid.uuid4().hex}.png"
        saved_image_path = history_folder / unique_filename

        with open(saved_image_path, "wb") as image_file:
            image_file.write(result)

        # Save the history record in the database.
        try:
            with get_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO tryon_history
                    (user_id, outfit_id, outfit_name, result_image)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        outfit["id"],
                        outfit["name"],
                        f"images/tryon_history/{unique_filename}",
                    ),
                )
        except Exception:
            saved_image_path.unlink(missing_ok=True)
            raise

        # Return the result to the existing frontend.
        return send_file(
            io.BytesIO(result),
            mimetype="image/png",
            download_name="styleverse-tryon.png",
            max_age=0,
        )


    except requests.RequestException:
        return jsonify({
            "error": "The AI service is unavailable. Make sure its terminal is running."
        }), 503
    except (UnidentifiedImageError, OSError):
        return jsonify({"error": "The AI service returned an invalid image."}), 502
