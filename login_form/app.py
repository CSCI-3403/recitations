from functools import lru_cache
import logging
import sys

import click
from flask import Flask, render_template, request, redirect, session, url_for

# Init logging
log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Init app
app = Flask(__name__)
app.secret_key = "asdigaskdlfha"

@app.route("/")
def index():
    if "id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    username_errors = []
    password_errors = []
    user = None

    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")

        if user is None:
            username_errors.append("Username is required")
        elif pw is None:
            password_errors.append("Password is required")
        elif (user, pw) != ("admin", "admin"):
            password_errors.append("Incorrect password")
        else:
            session["id"] = "admin"
            return redirect(url_for("index"))
    
    return render_template("login.html", username=user or "", username_errors=username_errors, password_errors=password_errors)

@click.command()
@click.option("--debug", is_flag=True)
@click.option("--port", type=int, default=80)
def main(debug: bool, port: int) -> None:
    app.run("0.0.0.0", debug=debug, port=port)

if __name__ == "__main__":
    main()
