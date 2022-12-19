"""Server for magic ingredients app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
import os
import requests

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['SPOONACULAR_APIKEY']
url = 'https://api.spoonacular.com/recipes'
HEADERS = {"Content-Type": "application/json"}

@app.route("/")
def homepage():
    """View homepage."""
    return render_template("homepage.html")

# @app.route("/users/<user_id>")
# def show_user(user_id):
#     """Show details on a particular user."""
#     user = crud.get_user_by_id(user_id)
#     return render_template('user_profiles.html', user=user)

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
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login_user():
    """Login user."""
    if request.method == "GET":
        return render_template('login.html')
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        print(f"EMAIL IS {email}")
        user = crud.get_user_by_email(email)
        if user and user.password == password:
            session["user_email"] = user.email
            session["user_id"] = user.user_id
            flash(f"Welcome back. {user.username}")
            return redirect(f"/user_home/{session['user_id']}")
        else:
            flash("Wrong combination.")
            return redirect("/login")
        
@app.route("/logout", methods=["POST"])
def process_logout():
    """Delete session and logout user"""
    session.clear()
    
    return redirect("/")

@app.route('/user_home/<user_id>')
def user_profile(user_id):
    """Show the User's homepage after login"""
    user = crud.get_user_by_id(user_id)
    #fav_recipes = crud.get_favorite_by_user(user_id)
    #shoppinglist = crud.get_shoppinglist_by_user(user_id)
    endpoint = '/random'
    final_url = url + endpoint
    data = {"number":"9", "apiKey": API_KEY}
    response = requests.get(final_url, headers=HEADERS, params=data).json()['recipes']
    print(response)
    # print(fav_recipes[0].recipe)
    # print(shoppinglist)

    return render_template('user_home.html', user=user, user_id=session['user_id'], recipes=response)

@app.route('/user_home/<user_id>')
def show_random_recipes():
    """show random recipes"""
    
    if response:
        return render_template('user_home.html', user_id=session['user_id'], recipes=response)


@app.route('/search', methods=["POST"])
def search_recipes():
    """search recipes based on input ingredients"""
    ingredients = request.form.get("search").replace(",", ",+")
    #print(ingredients)
    endpoint = '/findByIngredients'
    final_url = url + endpoint
    data = {"ingredients": ingredients, "apiKey": API_KEY}
    response = requests.get(final_url, headers=HEADERS, params=data).json()
    #print(response)
    if response:
        return render_template('recipe_results.html', user_id=session['user_id'], recipes=response)
    









if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)