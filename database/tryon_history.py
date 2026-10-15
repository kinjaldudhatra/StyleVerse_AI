
"""Create the StyleVerse AI virtual try-on history table."""

from models.database import get_connection


def create_tryon_history_table():
    """Create the history table without modifying existing tables."""

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tryon_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                outfit_id INTEGER,
                outfit_name TEXT NOT NULL,
                result_image TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (outfit_id) REFERENCES outfits(id)
                    ON DELETE SET NULL
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_tryon_history_user
            ON tryon_history(user_id, created_at)
        """)


if __name__ == "__main__":
    create_tryon_history_table()
    print("Virtual try-on history table is ready!")
