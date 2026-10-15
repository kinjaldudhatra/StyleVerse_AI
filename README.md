# StyleVerse AI

## Description

StyleVerse AI is an AI-powered fashion and beauty recommendation web application built as a college minor project. It is developed in phases. This repository currently contains Phase 1: the project foundation, the Flask backend and the SQLite database.

## Current Features

- Flask application with a clean, modular structure
- Responsive landing page (desktop, tablet and mobile)
- Custom 404 error page
- SQLite database with `users`, `outfits` and `makeup_products` tables
- Sample data: 5 female outfits, 5 male outfits and 10 makeup products
- Configurable secret key through an environment file
- User registration, login and logout with secure password hashing
- Session-based authentication, a reusable `@login_required` decorator and a temporary protected dashboard
- Navigation bar that changes depending on whether the user is logged in

Recommendations and virtual try-on are not implemented yet and will be added in later phases.

## Technology Stack

- Python 3
- Flask
- SQLite
- HTML5, CSS3 and JavaScript

## Project Structure

```
StyleVerse_AI/
├── app.py                 # Application factory and entry point
├── config.py              # Configuration loaded from environment variables
├── requirements.txt
├── .env.example           # Example environment file
├── database/
│   ├── init_db.py         # Creates tables and inserts sample data
│   └── fashion.db         # SQLite database (created by init_db.py)
├── models/
│   ├── database.py        # Reusable SQLite connection and query helpers
│   └── user.py            # User queries (find and create users)
├── routes/
│   ├── main.py            # Home page and temporary dashboard routes
│   └── auth.py            # Register, login and logout routes
├── utils/
│   ├── auth.py            # login_required decorator and safe redirect check
│   ├── csrf.py            # CSRF token helpers for forms
│   └── validators.py      # Form validation rules
├── services/              # Reserved for business logic in later phases
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── 404.html
└── static/
    ├── css/               # style.css, auth.css
    ├── js/                # main.js, auth.js
    └── images/            # outfits, makeup, backgrounds, logo
```

## Authentication

| Page | URL | Description |
|------|-----|-------------|
| Register | `/register` | Create an account |
| Login | `/login` | Start a session |
| Logout | `/logout` | End the session |
| Dashboard | `/dashboard` | Temporary page, login required |

**Registration.** Users enter a full name, email, password, password confirmation and gender. The server checks every field: the name must be 2 to 60 characters, the email must be valid, the password must have at least 8 characters including a letter and a number, and the two passwords must match. Emails are saved in lowercase, so `TEST@example.com` and `test@example.com` are the same account. Registering an email that already exists is refused.

**Login.** The email and password are checked against the database. A wrong email and a wrong password show the same message, "Invalid email or password.", so the form does not reveal which emails are registered. After a successful login the user is sent to the dashboard (or to the page they originally asked for).

**Logout.** `/logout` clears the session and returns to the home page with a confirmation message.

**Password hashing.** Passwords are never stored. Werkzeug's `generate_password_hash()` creates a salted hash, which is saved in the `password_hash` column, and `check_password_hash()` verifies it at login.

**Session management.** After login, Flask stores only `user_id` and `user_name` in a signed session cookie. Protected pages use the `@login_required` decorator in `utils/auth.py`; visitors who are not logged in are redirected to `/login`. Forms include a CSRF token, and redirects after login only accept paths on this site.

Set a long random `SECRET_KEY` in your `.env` file, because it is used to sign the session cookie.

## Installation

These steps are for Windows.

1. Create a virtual environment:

   ```
   python -m venv venv
   ```

2. Activate it:

   ```
   venv\Scripts\activate
   ```

3. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

4. (Optional) Create your own environment file and set a secret key:

   ```
   copy .env.example .env
   ```

5. Initialize the database:

   ```
   python database/init_db.py
   ```

6. Run the application:

   ```
   python app.py
   ```

7. Open this address in your browser:

   ```
   http://127.0.0.1:5000
   ```

The sample database is already included in the project. Running `init_db.py` again is safe: it will not create duplicate sample records.

## Troubleshooting

**Python is not recognized**
Reinstall Python from python.org and tick "Add Python to PATH" during installation. Then close and reopen the terminal. You can also try `py` instead of `python`.

**ModuleNotFoundError**
The virtual environment is probably not active, or the dependencies are not installed. Run `venv\Scripts\activate`, then `pip install -r requirements.txt`. Run the commands from the `StyleVerse_AI` folder.

**Port already in use**
Another program is using port 5000. Close it, or change the port in the last line of `app.py` (for example, `port=5001`) and open `http://127.0.0.1:5001`.
