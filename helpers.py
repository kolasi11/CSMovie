import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from dotenv import load_dotenv


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        load_dotenv()
        api_key = os.getenv("API_KEY")
        url = f"http://www.omdbapi.com/?s={urllib.parse.quote_plus(symbol)}&apikey={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {"search": quote["Search"], "totalResults": quote["totalResults"]}
    except (KeyError, TypeError, ValueError):
        return None


def look_title(movie_id):
    """look for movie id"""
    try:
        api_key = os.getenv("API_KEY")
        url = f"http://www.omdbapi.com/?i={urllib.parse.quote_plus(movie_id)}&plot=full&apikey={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "title": quote["Title"],
            "year": quote["Year"],
            "poster": quote["Poster"],
            "plot": quote["Plot"],
            "actors": quote["Actors"],
            "genres": quote["Genre"],
            "directors": quote["Director"],
            "writers": quote["Writer"],
            "languages": quote["Language"],
            "countries": quote["Country"],
            "runtime": quote["Runtime"],
            "rating": quote["imdbRating"],
            "type": quote["Type"],
            "release": quote["Released"],
            "imdbID": quote["imdbID"],
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
