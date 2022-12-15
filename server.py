"""Server for magic ingredients app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""
    user = crud.get_user_by_id(user_id)
    return render_template('user_profiles.html', user=user)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if user:
        flash("Email already exists. Try again")
    else:
        user = crud.create_user(username, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    return redirect("/")

@app.route("/login", methods=["POST"])
def login_user():
    """Login user."""
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if user and user.password == password:
        session["user_email"] = user.email
        flash(f"Welcome back. {user.username}")
        return show_user(user.user_id)
    else:
        flash("Wrong combination.")
    return redirect("/")










if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)