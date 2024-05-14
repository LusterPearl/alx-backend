#!/usr/bin/env python3
"""Flask app with user login emulation, locale, and timezone selection"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext as _
import pytz
from datetime import datetime


app = Flask(__name__)


class Config:
    """Configuration for flask-babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)

"""Mock user database"""
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id):
    """Retrieve a user from the mock database"""
    return users.get(user_id)


@app.before_request
def before_request():
    """Set the user as a global variable before each request"""
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None


@babel.localeselector
def get_locale():
    """Determine the best match with supported languages or use the forced locale."""
    url_locale = request.args.get('locale')
    if url_locale in app.config['LANGUAGES']:
        return url_locale
    
    """Priority 2: User settings"""
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']
    
    """Priority 3: Request header"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Determine the best match for time zone or use the forced time zone."""
    url_timezone = request.args.get('timezone')
    if url_timezone:
        try:
            pytz.timezone(url_timezone)
            return url_timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    
    """Priority 2: User settings"""
    if g.user:
        user_timezone = g.user.get('timezone')
        if user_timezone:
            try:
                pytz.timezone(user_timezone)
                return user_timezone
            except pytz.exceptions.UnknownTimeZoneError:
                pass
    
    """Default to UTC"""
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    """Route for the index page"""
    current_time = datetime.now(pytz.utc)
    user_timezone = get_timezone()
    localized_time = current_time.astimezone(pytz.timezone(user_timezone))
    return render_template('7-index.html', current_time=localized_time)


if __name__ == '__main__':
    app.run(debug=True)