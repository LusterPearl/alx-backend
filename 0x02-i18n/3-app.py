#!/usr/bin/env python3
"""Flask app with Babel locale selection and translations"""
from flask import Flask, render_template, request
from flask_babel import Babel, gettext as _
import pytz


class Config:
    """configuaration for flask-babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determine the best match with supported languages"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """Route for the index page"""
    current_time = datetime.now(pytz.utc)
    return render_template('3-index.html', current_time=current_time)


if __name__ == '__main__':
    app.run(debug=True)