
"""Safely add profile fields to the existing users table."""

from models.database import get_connection


def migrate_profile_fields():
    with get_connection() as connection:
        existing_columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(users)"
            ).fetchall()
        }

        new_columns = {
            "skin_tone": "TEXT",
            "face_shape": "TEXT",
            "clothing_size": "TEXT",
            "style_preference": "TEXT",
            "favorite_color": "TEXT",
            "preferred_occasion": "TEXT",
        }

        for column_name, column_type in new_columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    f"ALTER TABLE users ADD COLUMN "
                    f"{column_name} {column_type}"
                )

    print("Profile fields are ready!")


if __name__ == "__main__":
    migrate_profile_fields()
