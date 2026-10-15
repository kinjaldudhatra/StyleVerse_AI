from flask import Flask, render_template

from config import Config
from routes.auth import auth_bp
from routes.main import main_bp
from routes.fashion import fashion_bp
from routes.virtual_try_on import virtual_tryon_bp
from routes.tryon_history import tryon_history_bp
from routes.profile import profile_bp
from routes.jewellery import jewellery_bp
from routes.account_settings import account_settings_bp
from utils.csrf import generate_csrf_token


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(fashion_bp)
    app.register_blueprint(virtual_tryon_bp)
    app.register_blueprint(tryon_history_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(account_settings_bp)
    app.register_blueprint(jewellery_bp)
    app.jinja_env.globals["csrf_token"] = generate_csrf_token

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
