
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    flash,
)

from utils.auth import login_required
from models.database import get_connection
from utils.csrf import is_csrf_token_valid


fashion_bp = Blueprint(
    "fashion",
    __name__,
    url_prefix="/fashion"
)

@fashion_bp.route("/")
@login_required
def fashion_home():
    """Display outfits and the current user's wishlist status."""

    user_id = session["user_id"]

    try:
        with get_connection() as connection:
            outfits = connection.execute(
                """
                SELECT
                    id,
                    name,
                    gender,
                    category,
                    style,
                    color,
                    occasion,
                    season,
                    fit,
                    image,
                    description
                FROM outfits
                ORDER BY id
                """
            ).fetchall()

            saved_rows = connection.execute(
                """
                SELECT outfit_id
                FROM wishlist
                WHERE user_id = ?
                """,
                (user_id,)
            ).fetchall()

        saved_outfit_ids = {row["outfit_id"] for row in saved_rows}

        return render_template(
            "fashion.html",
            outfits=outfits,
            saved_outfit_ids=saved_outfit_ids
        )

    except Exception as error:
        print("Error loading outfits:", error)

        return render_template(
            "fashion.html",
            outfits=[],
            saved_outfit_ids=set()
        )


@fashion_bp.route("/recommend", methods=["POST"])
@login_required
def recommend_outfits():
    """Recommend outfits using normalized preference matching."""

    data = request.get_json(silent=True) or {}

    gender = str(data.get("gender", "")).strip()
    style = str(data.get("style", "")).strip()
    occasion = str(data.get("occasion", "")).strip()
    season = str(data.get("season", "")).strip()
    category = str(data.get("category", "")).strip()
    color = str(data.get("color", "")).strip()
    fit = str(data.get("fit", "")).strip()

    if not gender:
        return jsonify({
            "success": False,
            "message": "Please select your gender."
        }), 400

    def normalize(value):
        return " ".join(str(value or "").lower().replace("-", " ").split())

    # Connect common form choices with relevant database values.
    
    occasion_groups = {
        "college": {
            "college", "casual", "outing", "travel", "brunch"
        },
        "office": {
            "office", "formal", "business"
        },
        "party": {
            "party", "evening", "elegant"
        },
        "wedding": {
            "wedding", "formal", "festive", "festival",
            "traditional", "ethnic"
        },
        "festival": {
            "festival", "festive", "wedding",
            "traditional", "ethnic"
        },
        "festive": {
            "festive", "festival", "wedding",
            "traditional", "ethnic"
        },
        "outing": {
            "outing", "casual", "travel", "brunch"
        },
        "travel": {
            "travel", "outing", "casual"
        },
        "brunch": {
            "brunch", "casual", "outing"
        }
    }

    
    def occasion_matches(requested, stored):
        requested = normalize(requested)
        stored = normalize(stored)

        if not requested or not stored:
            return False

        if requested == stored:
            return True

        requested_group = occasion_groups.get(
            requested, {requested}
        )
        stored_group = occasion_groups.get(
            stored, {stored}
        )

        return (
            stored in requested_group
            or requested in stored_group
        )

    traditional_words = (
        "kurta", "kurti", "lehenga", "anarkali",
        "saree", "ethnic", "traditional", "churidar"
    )

    western_words = (
        "dress", "jeans", "denim", "western", "crop",
        "coord", "co ord", "jogger", "hoodie",
        "shirt", "chinos", "polo", "cargo", "gown"
    )

    
    
    def category_matches(outfit):
        requested = normalize(category)

        if not requested:
            return False

        outfit_category = normalize(outfit["category"])
        outfit_name = normalize(outfit["name"])
        searchable = " ".join([
            outfit_category,
            outfit_name,
            normalize(outfit["style"]),
            normalize(outfit["description"])
        ])

        category_groups = {
            "indian": (
                "anarkali", "kurta", "kurti", "lehenga",
                "saree", "sharara", "ethnic", "traditional"
            ),
            "ethnic wear": (
                "anarkali", "kurta", "kurti", "lehenga",
                "saree", "sharara", "ethnic", "traditional"
            ),
            "western": (
                "western", "dress", "gown", "blazer",
                "trousers", "jeans", "chinos", "hoodie",
                "cargo", "polo", "t-shirt", "co-ord set"
            ),
            "indo western": (
                "indo western", "fusion"
            ),
            "dress": ("dress", "gown"),
            "top jeans": ("shirt & jeans", "top & jeans", "jeans"),
            "co ord set": ("co-ord set", "coord set"),
            "suit": ("suit", "kurta set", "blazer & trousers"),
            "activewear": ("activewear", "sportswear", "workout")
        }

        if requested == outfit_category:
            return True

        requested = requested.replace("&", "and").replace("-", " ")
        if requested == "top and jeans":
            requested = "top jeans"
        if requested == "co ord set":
            terms = category_groups["co ord set"]
        else:
            terms = category_groups.get(requested, (requested,))

        if requested == "western":
            traditional_words = (
                "anarkali", "kurta", "kurti", "lehenga",
                "saree", "sharara"
            )
            if any(word in searchable for word in traditional_words):
                return False

        return any(normalize(term) in searchable for term in terms)

    try:
        with get_connection() as connection:
            outfits = connection.execute(
                """
                SELECT id, name, gender, category, style, color,
                       occasion, season, fit, image, description
                FROM outfits
                WHERE LOWER(TRIM(gender)) = LOWER(TRIM(?))
                ORDER BY id
                """,
                (gender,)
            ).fetchall()

        recommendations = []

        
        for outfit in outfits:

            # Exclude outfits that fail selected hard filters.
            if occasion and not occasion_matches(
                occasion, outfit["occasion"]
            ):
                continue

            if category and not category_matches(outfit):
                continue
            
            score = 0
            reasons = []

            outfit_style = normalize(outfit["style"])

            style_aliases = {
                "traditional": "ethnic",
                "evening": "elegant"
            }

            selected_style = style_aliases.get(
                normalize(style), normalize(style)
            )

            outfit_style = style_aliases.get(
                outfit_style, outfit_style
            )
            outfit_occasion = normalize(outfit["occasion"])
            outfit_season = normalize(outfit["season"])
            outfit_color = normalize(outfit["color"])
            outfit_fit = normalize(outfit["fit"])

            # Only count preferences the user selected.
            selected_weight = 0

            # Style: 30 points
            if style:
                selected_weight += 30
                if outfit_style == selected_style:
                    score += 30
                    reasons.append("Matches your preferred style")

            # Occasion: 25 points
            if occasion:
                selected_weight += 25
                if occasion_matches(occasion, outfit_occasion):
                    score += 25
                    reasons.append(f"Suitable for {occasion}")

            # Season: 15 points
            if season:
                selected_weight += 15
                if (
                    outfit_season == normalize(season)
                    or outfit_season in {"all season", "all seasons"}
                    or normalize(season) in {"all season", "all seasons"}
                ):
                    score += 15
                    reasons.append(f"Suitable for {season}")

            # Outfit category: 15 points
            if category:
                selected_weight += 15
                if category_matches(outfit):
                    score += 15
                    reasons.append(
                        f"Matches your {category} outfit preference"
                    )

            # Color: 10 points
            if color:
                selected_weight += 10
                if outfit_color == normalize(color):
                    score += 10
                    reasons.append(f"Matches your preferred {color} color")

            # Fit: 5 points
            if fit:
                selected_weight += 5
                if outfit_fit == normalize(fit):
                    score += 5
                    reasons.append(f"Matches your preferred {fit} fit")

            # Convert the weighted score to a percentage.
            match_percentage = (
                round(score / selected_weight * 100)
                if selected_weight else 0
            )

            recommendations.append({
                "id": outfit["id"],
                "name": outfit["name"],
                "gender": outfit["gender"],
                "category": outfit["category"],
                "style": outfit["style"],
                "color": outfit["color"],
                "occasion": outfit["occasion"],
                "season": outfit["season"],
                "fit": outfit["fit"],
                "image": outfit["image"],
                "description": outfit["description"],
                "score": match_percentage,
                "reasons": reasons,
                "why": (
                    " • ".join(reasons)
                    if reasons
                    else "A possible alternative from your selected gender category."
                )
            })

        recommendations.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return jsonify({
            "success": True,
            "recommendations": recommendations[:5]
        })

    except Exception as error:
        print("Fashion recommendation error:", error)
        return jsonify({
            "success": False,
            "message": "Unable to generate recommendations."
        }), 500

# ==========================================
# WISHLIST ROUTES
# ==========================================

@fashion_bp.route("/wishlist")
@login_required
def view_wishlist():
    """Display the current user's saved outfits."""

    user_id = session["user_id"]

    with get_connection() as connection:
        outfits = connection.execute(
            """
            SELECT
                outfits.id,
                outfits.name,
                outfits.gender,
                outfits.category,
                outfits.style,
                outfits.color,
                outfits.occasion,
                outfits.season,
                outfits.fit,
                outfits.image,
                outfits.description
            FROM wishlist
            JOIN outfits ON wishlist.outfit_id = outfits.id
            WHERE wishlist.user_id = ?
            ORDER BY wishlist.created_at DESC
            """,
            (user_id,)
        ).fetchall()

    return render_template("wishlist.html", outfits=outfits)


@fashion_bp.route("/wishlist/add/<int:outfit_id>", methods=["POST"])
@login_required
def add_to_wishlist(outfit_id):
    """Save an outfit and support both AJAX and normal form requests."""

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if not is_csrf_token_valid():
        if is_ajax:
            return jsonify({
                "success": False,
                "message": "Your session expired. Please refresh and try again."
            }), 400

        flash("Your session expired. Please try again.", "error")
        return redirect(url_for("fashion.fashion_home"))

    user_id = session["user_id"]

    with get_connection() as connection:
        outfit = connection.execute(
            "SELECT id FROM outfits WHERE id = ?",
            (outfit_id,)
        ).fetchone()

        if outfit is None:
            if is_ajax:
                return jsonify({
                    "success": False,
                    "message": "Outfit not found."
                }), 404

            flash("Outfit not found.", "error")
            return redirect(url_for("fashion.fashion_home"))

        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO wishlist (user_id, outfit_id)
            VALUES (?, ?)
            """,
            (user_id, outfit_id)
        )

        was_added = cursor.rowcount == 1

    message = (
        "Outfit saved to your wishlist! ❤️"
        if was_added
        else "This outfit is already in your wishlist."
    )

    if is_ajax:
        return jsonify({
            "success": True,
            "saved": True,
            "already_saved": not was_added,
            "outfit_id": outfit_id,
            "message": message
        })

    flash(message, "success")
    return redirect(request.referrer or url_for("fashion.fashion_home"))


@fashion_bp.route(
    "/wishlist/remove/<int:outfit_id>",
    methods=["POST"]
)
@login_required
def remove_from_wishlist(outfit_id):
    """Remove an outfit from the current user's wishlist."""

    if not is_csrf_token_valid():
        flash("Your session expired. Please try again.", "error")
        return redirect(url_for("fashion.view_wishlist"))

    user_id = session["user_id"]

    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM wishlist
            WHERE user_id = ? AND outfit_id = ?
            """,
            (user_id, outfit_id)
        )

    flash("Outfit removed from your wishlist.", "success")
    return redirect(url_for("fashion.view_wishlist"))
