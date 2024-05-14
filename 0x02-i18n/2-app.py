#!/usr/bin/env python3
"""Flask app with Babel locale selection"""
from flask import Flask, render_template, request
from flask_babel import Babel


class config:
    """
    configuratio for flask Babel
    """
    LANGUAGES = ["en" "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)


babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determine the best match ith supported languages"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """route for the index page"""
    return render_template('2_index.html')


if __name__ == '__main__':
    app.run(debug=True)
