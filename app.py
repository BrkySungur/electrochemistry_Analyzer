"""
Application entry point.

Creates the Flask app via the factory function and registers all
module blueprints. Run directly with:

    python app.py

or via a WSGI server:

    gunicorn "app:create_app()"
"""

from __future__ import annotations

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

from config import Config
from modules.gcd.routes import gcd_bp

csrf = CSRFProtect()


def create_app(config_object: object = Config) -> Flask:
    """
    Flask application factory.

    Args:
        config_object: A configuration class (defaults to
                       :class:`config.Config`).

    Returns:
        A fully initialised :class:`flask.Flask` instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Extensions
    csrf.init_app(app)

    # Blueprints
    app.register_blueprint(gcd_bp)

    # Root route
    @app.route("/")
    def home():
        return render_template("home.html")

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=application.config["DEBUG"], load_dotenv=True)
