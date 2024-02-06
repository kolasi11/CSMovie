import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, look_title, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///cinema.db")




@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/index", methods=["GET", "POST"])
def quote():
    """Search movie name."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if lookup(symbol) != None:
            return render_template("quoted.html", results=lookup(symbol))
        else:
            return apology("Name doesn't exist", 400)

    else:
        # Redirect user to home page
        return render_template("/index.html")


@app.route("/details", methods=["GET", "POST"])
def details():
    """Get movie details."""
    movie_id = request.args.get("type")
    if look_title(movie_id) != None:
        return render_template("details.html", result=look_title(movie_id))
    else:
        return apology("Name doesn't exist", 400)


@app.route("/add_to_watchlist/<movie_id>", methods=["POST"])
@login_required
def add_movie(movie_id):
    """Add movies to user's watchlist."""
    user_movies = []
    rows = db.execute(
        "SELECT movie_id FROM watchlist WHERE user_id = ?", session["user_id"]
    )
    for row in rows:
        user_movies.append(row["movie_id"])

    movie_name = look_title(movie_id)["title"]

    if movie_id in user_movies:
        return apology("Movie is already in watchlist", 400)
    else:
        db.execute(
            "INSERT INTO watchlist (user_id, movie_id, movie_name) VALUES(?, ?, ?)",
            session["user_id"],
            [movie_id],
            movie_name,
        )
        return render_template("details.html", result=look_title(movie_id))


@app.route("/watchlist", methods=["GET", "POST"])
@login_required
def watchlist():
    """Show user watchlist"""

    movie_id = request.args.get("type")
    db.execute(
        "DELETE FROM watchlist WHERE user_id = ? AND movie_id = ?",
        session["user_id"],
        movie_id,
    )

    watchlist = db.execute(
        "SELECT * FROM watchlist WHERE user_id = ?", session["user_id"]
    )

    return render_template("watchlist.html", watchlist=watchlist)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        user = request.form.get("username")
        password = request.form.get("password")
        check = db.execute("SELECT username FROM users where username == ?", user)

        # Ensure username was submitted
        if not user:
            return apology("must provide username", 400)

        # Ensure username isn't taken
        elif len(check) != 0:
            return apology("username taken", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure confirm password was similar to password
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("both password should be same", 400)

        # hashes the user password for security
        hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)

        # Stores the username and hash in database
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", user, hash)

        # Remember which user has logged in
        info = db.execute("SELECT * FROM users WHERE username = ?", user)
        id = info[0]["id"]
        session["user_id"] = id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
