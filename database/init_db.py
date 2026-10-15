import sqlite3
import os


# ---------------------------------------------------------
# Database path
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "fashion.db")


# ---------------------------------------------------------
# Outfit data
# ---------------------------------------------------------

outfits = [

    # =====================================================
    # FEMALE OUTFITS
    # =====================================================

    {
        "name": "Floral Wrap Dress",
        "gender": "Female",
        "category": "Dress",
        "style": "Casual",
        "color": "Pink",
        "occasion": "Casual",
        "season": "Summer",
        "fit": "Regular",
        "image": "floral-wrap-dress.jpg",
        "description": "A feminine floral wrap dress perfect for casual summer outings and daytime occasions."
    },

    {
        "name": "Linen Co-ord Set",
        "gender": "Female",
        "category": "Co-ord Set",
        "style": "Casual",
        "color": "Beige",
        "occasion": "Casual",
        "season": "Summer",
        "fit": "Relaxed",
        "image": "linen-coord-set.jpg",
        "description": "A comfortable beige linen co-ord set offering a clean and effortless summer look."
    },

    {
        "name": "Satin Slip Dress",
        "gender": "Female",
        "category": "Dress",
        "style": "Elegant",
        "color": "Blue",
        "occasion": "Party",
        "season": "All Season",
        "fit": "Slim",
        "image": "satin-slip-dress.jpg",
        "description": "An elegant satin slip dress designed for parties, dinners and evening occasions."
    },

    {
        "name": "Denim Crop Set",
        "gender": "Female",
        "category": "Co-ord Set",
        "style": "Casual",
        "color": "Blue",
        "occasion": "College",
        "season": "Summer",
        "fit": "Regular",
        "image": "denim-crop-set.jpg",
        "description": "A trendy denim crop set suitable for college, casual outings and everyday wear."
    },

    {
        "name": "Embroidered Kurti",
        "gender": "Female",
        "category": "Kurti",
        "style": "Ethnic",
        "color": "Yellow",
        "occasion": "Festive",
        "season": "Summer",
        "fit": "Regular",
        "image": "embroidered-kurti.jpg",
        "description": "A bright embroidered kurti suitable for festive celebrations and traditional occasions."
    },

    {
        "name": "Red Wrap Dress",
        "gender": "Female",
        "category": "Dress",
        "style": "Elegant",
        "color": "Red",
        "occasion": "Party",
        "season": "All Season",
        "fit": "Slim",
        "image": "red-wrap-dress.jpg",
        "description": "A stylish red wrap dress perfect for parties, dates and evening events."
    },

    {
        "name": "Lavender Wrap Dress",
        "gender": "Female",
        "category": "Dress",
        "style": "Elegant",
        "color": "Purple",
        "occasion": "Party",
        "season": "Summer",
        "fit": "Regular",
        "image": "lavender-wrap-dress.jpg",
        "description": "A soft lavender wrap dress creating an elegant and graceful party look."
    },

    {
        "name": "Anarkali Suit",
        "gender": "Female",
        "category": "Anarkali",
        "style": "Ethnic",
        "color": "Cream",
        "occasion": "Wedding",
        "season": "All Season",
        "fit": "Regular",
        "image": "anarkali-suit.jpg",
        "description": "A graceful traditional Anarkali suit ideal for weddings and festive celebrations."
    },

    {
        "name": "Lehenga",
        "gender": "Female",
        "category": "Lehenga",
        "style": "Ethnic",
        "color": "Green",
        "occasion": "Wedding",
        "season": "All Season",
        "fit": "Regular",
        "image": "lehenga.jpg",
        "description": "A beautiful green lehenga designed for weddings, receptions and festive occasions."
    },

    {
        "name": "Evening Gown",
        "gender": "Female",
        "category": "Gown",
        "style": "Elegant",
        "color": "Black",
        "occasion": "Party",
        "season": "All Season",
        "fit": "Slim",
        "image": "evening-gown.jpg",
        "description": "A sophisticated black evening gown perfect for formal parties and evening events."
    },

    {
        "name": "Blue Jacket Skort",
        "gender": "Female",
        "category": "Co-ord Set",
        "style": "Casual",
        "color": "Blue",
        "occasion": "College",
        "season": "Summer",
        "fit": "Regular",
        "image": "blue-jacket-skort.png",
        "description": "A fashionable blue jacket and skort combination suitable for college and casual outings."
    },

    {
        "name": "Blue Kurta Lehenga",
        "gender": "Female",
        "category": "Lehenga",
        "style": "Ethnic",
        "color": "Blue",
        "occasion": "Wedding",
        "season": "All Season",
        "fit": "Regular",
        "image": "blue-kurta-lahenga.png",
        "description": "A stylish blue traditional outfit suitable for weddings and festive celebrations."
    },

    {
        "name": "Blue Short Kurti",
        "gender": "Female",
        "category": "Kurti",
        "style": "Ethnic",
        "color": "Blue",
        "occasion": "Casual",
        "season": "Summer",
        "fit": "Regular",
        "image": "blue-short-kurti.png",
        "description": "A simple blue short kurti perfect for everyday ethnic and casual styling."
    },

    {
        "name": "Striped Co-ord Set",
        "gender": "Female",
        "category": "Co-ord Set",
        "style": "Casual",
        "color": "Blue",
        "occasion": "College",
        "season": "Summer",
        "fit": "Regular",
        "image": "blue-striped-coord-set.png",
        "description": "A modern striped co-ord outfit ideal for college and relaxed daytime looks."
    },

    {
        "name": "Champagne Embroidered Lehenga",
        "gender": "Female",
        "category": "Lehenga",
        "style": "Ethnic",
        "color": "Cream",
        "occasion": "Wedding",
        "season": "All Season",
        "fit": "Regular",
        "image": "champagne-embroidered-lehenga.png",
        "description": "An elegant champagne embroidered lehenga designed for weddings and special celebrations."
    },

    {
        "name": "Crop Top Leather Jacket",
        "gender": "Female",
        "category": "Western",
        "style": "Trendy",
        "color": "Black",
        "occasion": "Party",
        "season": "Winter",
        "fit": "Slim",
        "image": "crop-top-leather-jacket.png",
        "description": "A bold crop top and leather jacket combination for trendy party and evening looks."
    },

    {
        "name": "Crop Top Wide Leg Jeans",
        "gender": "Female",
        "category": "Western",
        "style": "Casual",
        "color": "Blue",
        "occasion": "College",
        "season": "All Season",
        "fit": "Relaxed",
        "image": "crop-top-wide-leg-jeans.png",
        "description": "A trendy crop top paired with wide-leg jeans for a comfortable everyday look."
    },

    {
        "name": "Hot Pink Embroidered Lehenga",
        "gender": "Female",
        "category": "Lehenga",
        "style": "Ethnic",
        "color": "Pink",
        "occasion": "Wedding",
        "season": "All Season",
        "fit": "Regular",
        "image": "hot-pink-embroidered-lehenga.png",
        "description": "A vibrant hot pink embroidered lehenga perfect for weddings and festive celebrations."
    },

    {
        "name": "Lavender Silk Saree",
        "gender": "Female",
        "category": "Saree",
        "style": "Ethnic",
        "color": "Purple",
        "occasion": "Wedding",
        "season": "All Season",
        "fit": "Regular",
        "image": "lavender-silk-saree.png",
        "description": "A graceful lavender silk saree suitable for weddings and elegant traditional events."
    },

    {
        "name": "Magenta Crochet White Skirt",
        "gender": "Female",
        "category": "Western",
        "style": "Trendy",
        "color": "Pink",
        "occasion": "Party",
        "season": "Summer",
        "fit": "Regular",
        "image": "magenta-crochet-white-skirt.png",
        "description": "A stylish magenta crochet top with a white skirt for trendy summer occasions."
    },

    {
        "name": "Maroon Draped Skirt Crop Top",
        "gender": "Female",
        "category": "Western",
        "style": "Trendy",
        "color": "Maroon",
        "occasion": "Party",
        "season": "All Season",
        "fit": "Slim",
        "image": "maroon-draped-skirt-crop-top.png",
        "description": "A fashionable maroon draped skirt and crop top combination for parties and celebrations."
    },

    {
        "name": "Maroon Embroidered Anarkali",
        "gender": "Female",
        "category": "Anarkali",
        "style": "Ethnic",
        "color": "Maroon",
        "occasion": "Wedding",
        "season": "All Season",
        "fit": "Regular",
        "image": "maroon-embroidered-anarkali.png",
        "description": "A richly embroidered maroon Anarkali perfect for weddings and traditional functions."
    },

    {
        "name": "Mint Green Sharara Set",
        "gender": "Female",
        "category": "Sharara",
        "style": "Ethnic",
        "color": "Green",
        "occasion": "Wedding",
        "season": "Summer",
        "fit": "Regular",
        "image": "mint-green-sharara-set.png",
        "description": "A refreshing mint green sharara set suitable for festive and wedding celebrations."
    },

    {
        "name": "Olive Kurta Palazzo",
        "gender": "Female",
        "category": "Kurta Set",
        "style": "Ethnic",
        "color": "Green",
        "occasion": "Casual",
        "season": "Summer",
        "fit": "Relaxed",
        "image": "olive-kurta-palazzo.png",
        "description": "A comfortable olive kurta and palazzo combination for everyday ethnic styling."
    },

    {
        "name": "Pink Gingham Mini Dress",
        "gender": "Female",
        "category": "Dress",
        "style": "Casual",
        "color": "Pink",
        "occasion": "Casual",
        "season": "Summer",
        "fit": "Regular",
        "image": "pink-gingham-mini-dress.png",
        "description": "A cute pink gingham mini dress perfect for casual summer outings."
    },

    {
        "name": "Pink Top Blue Jeans",
        "gender": "Female",
        "category": "Western",
        "style": "Casual",
        "color": "Pink",
        "occasion": "College",
        "season": "All Season",
        "fit": "Regular",
        "image": "pink-top-blue-jeans.png",
        "description": "A simple pink top with blue jeans for a comfortable college and casual look."
    },

    {
        "name": "White Dress",
        "gender": "Female",
        "category": "Dress",
        "style": "Elegant",
        "color": "White",
        "occasion": "Casual",
        "season": "Summer",
        "fit": "Regular",
        "image": "white-dress.png",
        "description": "A clean white dress offering a minimal and elegant summer appearance."
    },

    {
        "name": "White Tank Wide Leg Jeans",
        "gender": "Female",
        "category": "Western",
        "style": "Casual",
        "color": "White",
        "occasion": "College",
        "season": "Summer",
        "fit": "Relaxed",
        "image": "white-tank-wide-leg-jeans.png",
        "description": "A relaxed white tank and wide-leg jeans outfit for casual everyday styling."
    },


    # =====================================================
    # MALE OUTFITS
    # =====================================================

    {
        "name": "Navy Two Piece Suit",
        "gender": "Male",
        "category": "Suit",
        "style": "Formal",
        "color": "Navy",
        "occasion": "Office",
        "season": "All Season",
        "fit": "Slim",
        "image": "navy-two-piece-suit.jpg",
        "description": "A sophisticated navy two-piece suit ideal for formal meetings, office events and business occasions."
    },

    {
        "name": "Oxford Shirt Chinos",
        "gender": "Male",
        "category": "Shirt & Chinos",
        "style": "Smart Casual",
        "color": "Blue",
        "occasion": "Office",
        "season": "Summer",
        "fit": "Regular",
        "image": "oxford-shirt-chinos.jpg",
        "description": "A classic Oxford shirt and chinos combination for smart office and semi-formal occasions."
    },

    {
        "name": "Graphic Tee Cargo",
        "gender": "Male",
        "category": "T-Shirt & Cargo",
        "style": "Casual",
        "color": "Green",
        "occasion": "College",
        "season": "All Season",
        "fit": "Relaxed",
        "image": "graphic-tee-cargo.jpg",
        "description": "A relaxed graphic tee and cargo pants combination for casual college and everyday wear."
    },

    {
        "name": "Cotton Kurta Churidar",
        "gender": "Male",
        "category": "Kurta",
        "style": "Ethnic",
        "color": "Cream",
        "occasion": "Wedding",
        "season": "Summer",
        "fit": "Regular",
        "image": "cotton-kurta-churidar.jpg",
        "description": "A traditional cotton kurta and churidar combination suitable for weddings and festive occasions."
    },

    {
        "name": "Bomber Jogger Set",
        "gender": "Male",
        "category": "Co-ord Set",
        "style": "Streetwear",
        "color": "Black",
        "occasion": "Casual",
        "season": "Winter",
        "fit": "Relaxed",
        "image": "bomber-jogger-set.jpg",
        "description": "A modern black bomber and jogger set designed for casual streetwear styling."
    },

    {
        "name": "Hoodie Cargo Set",
        "gender": "Male",
        "category": "Hoodie & Cargo",
        "style": "Streetwear",
        "color": "Black",
        "occasion": "College",
        "season": "Winter",
        "fit": "Relaxed",
        "image": "hoodie-cargo-set.jpg",
        "description": "A comfortable hoodie and cargo combination ideal for college, casual outings and winter streetwear."
    },

    {
        "name": "Polo Chinos",
        "gender": "Male",
        "category": "Polo & Chinos",
        "style": "Smart Casual",
        "color": "Blue",
        "occasion": "Casual",
        "season": "Summer",
        "fit": "Regular",
        "image": "polo-chinos.jpg",
        "description": "A classic blue polo and chinos combination suitable for casual and smart-casual occasions."
    },

    {
        "name": "Shirt Jeans",
        "gender": "Male",
        "category": "Shirt & Jeans",
        "style": "Casual",
        "color": "White",
        "occasion": "College",
        "season": "All Season",
        "fit": "Regular",
        "image": "shirt-jeans.jpg",
        "description": "A clean white shirt and jeans combination for everyday casual and college wear."
    },

    {
        "name": "Beige Blazer Trouser Set",
        "gender": "Male",
        "category": "Blazer & Trousers",
        "style": "Formal",
        "color": "Beige",
        "occasion": "Office",
        "season": "All Season",
        "fit": "Slim",
        "image": "beige-blazer-trouser-set.png",
        "description": "A refined beige blazer and trouser combination for formal and business-casual occasions."
    },

    {
        "name": "Blue Striped Casual Set",
        "gender": "Male",
        "category": "Shirt & Trousers",
        "style": "Smart Casual",
        "color": "Blue",
        "occasion": "Casual",
        "season": "Summer",
        "fit": "Regular",
        "image": "blue-striped-coord-set.png",
        "description": "A stylish blue striped outfit offering a polished smart-casual appearance."
    }
]


# ---------------------------------------------------------
# Create database
# ---------------------------------------------------------

def initialize_database():

    # Create database folder if it does not exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Remove old outfits table
    cursor.execute("DROP TABLE IF EXISTS outfits")

    # Create new outfits table
    cursor.execute("""
        CREATE TABLE outfits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            category TEXT NOT NULL,
            style TEXT NOT NULL,
            color TEXT NOT NULL,
            occasion TEXT NOT NULL,
            season TEXT NOT NULL,
            fit TEXT NOT NULL,
            image TEXT NOT NULL,
            description TEXT
        )
    """)

    # Insert all outfit records
    for outfit in outfits:

        cursor.execute("""
            INSERT INTO outfits
            (
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
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            outfit["name"],
            outfit["gender"],
            outfit["category"],
            outfit["style"],
            outfit["color"],
            outfit["occasion"],
            outfit["season"],
            outfit["fit"],
            outfit["image"],
            outfit["description"]
        ))

    connection.commit()
    
    # Create wishlist table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            outfit_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id) REFERENCES users(id)
                ON DELETE CASCADE,

            FOREIGN KEY (outfit_id) REFERENCES outfits(id)
                ON DELETE CASCADE,

            UNIQUE (user_id, outfit_id)
        )
    """)


    connection.commit()

    # Show number of inserted outfits
    cursor.execute("SELECT COUNT(*) FROM outfits")
    count = cursor.fetchone()[0]

    connection.close()

    print("========================================")
    print(" StyleVerse AI Fashion Database")
    print("========================================")
    print(f"Database created successfully!")
    print(f"Total outfits inserted: {count}")
    print("========================================")


# ---------------------------------------------------------
# Run database initialization
# ---------------------------------------------------------

if __name__ == "__main__":
    initialize_database()