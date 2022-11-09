from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def inbox():
    """Show Received Emails"""
    userID = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userID)
    # we did this to have the value itself not the whole list like here in the dictionary [{"username":karimayman1298@gmail.com}]
    username = usernameDB[0]["username"]
    emails = db.execute("SELECT * FROM emails WHERE recipient = ?", username)
    return render_template("inbox.html", emails=emails)


@app.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    """Write a new Email"""
    if request.method == "GET":
        userId = session["user_id"]
        senderDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
        sender = senderDB[0]["username"]
        return render_template("compose.html", sender=sender)

    else:
        sender = request.form.get("sender")
        recipient = request.form.get("recipient")
        subject = request.form.get("subject")
        body = request.form.get("body")

        if not sender or not recipient or not subject or not body:
            return apology("No Empty Fields !")
        #INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);
        db.execute("INSERT INTO emails (sender, recipient, subject, body) VALUES (?, ?, ?, ?)", sender, recipient, subject, body)

        return redirect("/sent")



@app.route("/sent")
@login_required
def sent():
    """Show Sent Emails"""
    userID = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userID)
    # we did this to have the value itself not the whole list like here in the dictionary [{"username":karimayman1298@gmail.com}]
    username = usernameDB[0]["username"]
    emails = db.execute("SELECT * FROM emails WHERE sender = ?", username)
    return render_template("sent.html", emails=emails)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid email and/or password", 403)

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


@app.route("/email", methods=["GET", "POST"])
@login_required
def email():
    """View Email Details"""
    if request.method == "POST":
        emailId = request.form.get("emailId")
        emailDetailDB = db.execute("SELECT * from emails WHERE id = ?", emailId)
        # we did this to have the value itself not the whole list like here in the dictionary using jsonify(emailDetailDB) [{"body":"....", "id":"...."}] so we use to access the data with curly braces {} so we removed the brackets []
        emailDetail = emailDetailDB[0]
        return render_template("email.html", emailDetail=emailDetail)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        email = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not email or not password or not confirm :
            return apology("No Empty Fields !")

        if password != confirm :
            return apology("Password Do Not Match !")

        hash = generate_password_hash(password)

        try:
            #INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);
            newUser = db.execute("INSERT INTO users (username, hash) VALUES (? ,?)", email, hash)
        except:
            return apology("Email Already Used !")

        session["user_id"] = newUser

        return redirect("/")


@app.route("/reply", methods=["GET", "POST"])
@login_required
def reply():
    """Reply the email on email detail view"""
    if request.method == "POST":
        emailId = request.form.get("emailId")
        emailDetailDB = db.execute("SELECT * from emails WHERE id = ?", emailId)
        # we did this to have the value itself not the whole list like here in the dictionary using jsonify(emailDetailDB) [{"body":"....", "id":"...."}] so we use to access the data with curly braces {} so we removed the brackets []
        emailDetail = emailDetailDB[0]
        return render_template("reply.html", emailDetail=emailDetail)
