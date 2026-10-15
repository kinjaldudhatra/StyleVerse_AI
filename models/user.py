import sqlite3
from contextlib import closing

from models.database import fetch_one, get_connection
from werkzeug.security import check_password_hash, generate_password_hash

class EmailAlreadyRegisteredError(Exception):
    """Raised when an account with the same email address already exists."""


def get_user_by_email(email):
    """Return the user with the given normalized email, or None."""
    return fetch_one(
        "SELECT id, name, email, password_hash, gender, created_at "
        "FROM users WHERE lower(email) = ?",
        (email,),
    )


def get_user_by_id(user_id):
    """Return the user with the given id, or None."""
    return fetch_one(
        "SELECT id, name, email, gender, created_at FROM users WHERE id = ?",
        (user_id,),
    )


def create_user(name, email, password_hash, gender):
    """Insert a new user and return the new user id."""
    try:
        with closing(get_connection()) as connection:
            cursor = connection.execute(
                "INSERT INTO users (name, email, password_hash, gender) "
                "VALUES (?, ?, ?, ?)",
                (name, email, password_hash, gender),
            )
            connection.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError as error:
        raise EmailAlreadyRegisteredError(email) from error


def get_user_profile(user_id):
    """Return profile details for a specific user."""
    return fetch_one(
        """
        SELECT
            id,
            name,
            email,
            gender,
            skin_tone,
            face_shape,
            clothing_size,
            style_preference,
            favorite_color,
            preferred_occasion,
            created_at
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    )


def update_user_profile(
    user_id,
    name,
    gender,
    skin_tone,
    face_shape,
    clothing_size,
    style_preference,
    favorite_color,
    preferred_occasion,
):
    """Update editable profile details for one user."""
    with closing(get_connection()) as connection:
        connection.execute(
            """
            UPDATE users
            SET
                name = ?,
                gender = ?,
                skin_tone = ?,
                face_shape = ?,
                clothing_size = ?,
                style_preference = ?,
                favorite_color = ?,
                preferred_occasion = ?
            WHERE id = ?
            """,
            (
                name,
                gender,
                skin_tone,
                face_shape,
                clothing_size,
                style_preference,
                favorite_color,
                preferred_occasion,
                user_id,
            ),
        )
        connection.commit()


def change_user_password(user_id, current_password, new_password):
    """Change a user's password after verifying the current password."""
    user = fetch_one(
        "SELECT password_hash FROM users WHERE id = ?",
        (user_id,),
    )

    if user is None:
        return False, "Account not found."

    if not check_password_hash(user["password_hash"], current_password):
        return False, "Your current password is incorrect."

    new_password_hash = generate_password_hash(new_password)

    with closing(get_connection()) as connection:
        connection.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (new_password_hash, user_id),
        )
        connection.commit()

    return True, "Your password has been changed successfully."
