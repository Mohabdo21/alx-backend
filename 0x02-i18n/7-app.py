#!/usr/bin/env python3
""" Basic Flask app """
import pytz
from flask import Flask, g, render_template, request
from flask_babel import Babel
from pytz.exceptions import UnknownTimeZoneError


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
    # Locale from URL parameters
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale
    # Locale from user settings
    user = get_user()
    if user and user["locale"] in app.config["LANGUAGES"]:
        return user["locale"]
    # Locale from request header
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone():
    """Determine the best match with our supported timezones"""
    try:
        # Timezone from URL parameters
        timezone = request.args.get("timezone")
        if timezone:
            tz = pytz.timezone(timezone)
            return tz.zone
        # Timezone from user settings
        user = get_user()
        if user and user["timezone"]:
            tz = pytz.timezone(user["timezone"])
            return tz.zone
    except UnknownTimeZoneError:
        pass
    # Default timezone
    return "UTC"


@app.route("/")
def index():
    """Route for index page"""
    return render_template("6-index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")
