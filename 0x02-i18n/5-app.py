#!/usr/bin/env python3
""" Basic Flask app """
from flask import Flask, g, render_template, request
from flask_babel import Babel


class Config(object):
    """Configuration class for Babel"""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Returns a user dictionary or None"""
    user_id = request.args.get("login_as")
    if user_id is not None:
        user_id = int(user_id)
        return users.get(user_id)
    return None


@app.before_request
def before_request():
    """Executes before all other functions"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best match with our supported languages"""
    locale = request.args.get("locale")
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index():
    """Route for index page"""
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")
