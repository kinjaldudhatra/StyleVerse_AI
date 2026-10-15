
from flask import Blueprint, render_template
from utils.auth import login_required

jewellery_bp = Blueprint(
    "jewellery",
    __name__,
    url_prefix="/jewellery"
)


@jewellery_bp.route("/")
@login_required
def jewellery_home():
    """Display the StyleVerse AI jewellery collection."""
    jewellery_items = [
        {
            "name": "Pearl Elegance",
            "category": "Earrings",
            "description": "Timeless pearls for graceful everyday styling.",
            "icon": "✧",
            "style": "pearl"
        },
        {
            "name": "Golden Glow",
            "category": "Necklaces",
            "description": "Warm golden accents for a polished look.",
            "icon": "◇",
            "style": "gold"
        },
        {
            "name": "Rose Charm",
            "category": "Bracelets",
            "description": "Delicate details for a soft, elegant finish.",
            "icon": "❀",
            "style": "rose"
        },
        {
            "name": "Royal Sparkle",
            "category": "Rings",
            "description": "A statement piece for special occasions.",
            "icon": "✦",
            "style": "sparkle"
        },
        {
            "name": "Traditional Grace",
            "category": "Traditional",
            "description": "Jewellery inspiration for festive and ethnic outfits.",
            "icon": "❋",
            "style": "traditional"
        },
        {
            "name": "Minimal Muse",
            "category": "Minimal",
            "description": "Simple accessories that work with everyday looks.",
            "icon": "∞",
            "style": "minimal"
        }
    ]

    return render_template(
        "jewellery.html",
        jewellery_items=jewellery_items
    )
