"""Server for magic ingredients app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
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
            session["user_name"] = user.username
            #flash(f"Welcome back. {user.username}")
            return redirect(f"/user_home/{session['user_id']}")
        else:
            flash("Wrong combination.")
            return redirect("/login")
        
@app.route("/logout")
def process_logout():
    """Delete session and logout user"""
    del session["user_id"]
    del session["user_name"]
    del session["user_email"]
    
    return redirect("/")

@app.route('/user_home/<user_id>')
def user_profile(user_id):
    """Show the User's homepage after login"""
    user = crud.get_user_by_id(user_id)
    #fav_recipes = crud.get_favorite_by_user(user_id)
    #shoppinglist = crud.get_shoppinglist_by_user(user_id)
    """Show random recipes"""
    endpoint = '/random'
    final_url = url + endpoint
    data = {"number":"9", "apiKey": API_KEY}
    response = requests.get(final_url, headers=HEADERS, params=data).json()['recipes']
    # print(response)
    # print(fav_recipes[0].recipe)
    # print(shoppinglist)

    return render_template('user_home.html', user=user, user_id=session['user_id'], recipes=response)

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
    
@app .route('/recipe')
def show_recipe_detail():
    """Display recipe detail when click the recipe name."""
    recipe_id = request.args['id']
    endpoint = f"/{recipe_id}/information"
    final_url = url + endpoint
    print(final_url)
    
    data = {"includeNutrition":"false", "apiKey": API_KEY}
    response = requests.get(final_url, headers=HEADERS, params=data).json()
    print(response)
    
    cook_time = response['readyInMinutes']
    recipe_title = response['title']
    recipe_image = response['image']
    source_name = response['sourceName']
    source_url = response['sourceUrl']
    ingredient_list = response['extendedIngredients']
    ingredients = []
    recipe_ingredient = ""
    for ingredient in ingredient_list:
        ingredients.append({"ingredient_name": ingredient['original'], "ingredient_id": ingredient['id'], "ingredient_amount": ingredient['amount']})
        recipe_ingredient += ingredient['original']
    
    analyzed_instructions = response['analyzedInstructions']
    if not analyzed_instructions:
        steps = f"Read the detailed instructions on {source_name} - Click original link below"
        recipe_steps = steps
    else:
        instructions = analyzed_instructions[0]['steps']
        steps = []
        for step in instructions:
            steps.append(step['step'])
        recipe_steps = ",".join(steps)
    
    if not crud.get_recipe_by_api_id(recipe_id):
        new_recipe = crud.create_recipe(recipe_id, recipe_title, recipe_ingredient, recipe_image, recipe_steps, cook_time)
        db.session.add(new_recipe)
        db.session.commit()
    local_recipe = crud.get_recipe_by_api_id(recipe_id)
    return render_template('recipe_detail.html', user_id=session['user_id'], recipe=response,cook_time=cook_time, source_url=source_url, recipe_title=recipe_title, recipe_image=recipe_image,ingredients=ingredients, steps=steps, local_recipe_id=local_recipe.recipe_id)

@app.route('/favorites', methods=["GET", "POST"])
def favorite_recipes():
    """get favorite recipes"""
    if request.method == "GET":
        fav_recipes = crud.get_favorite_by_user(session['user_id'])
        recipes = []
        if fav_recipes:
            for fav_recipe in fav_recipes:
                recipe = crud.get_recipe_by_id(fav_recipe.recipe_id)
                recipes.append(recipe)
    else:
        search_fav = request.form.get("search_fav")
        fav_recipes = crud.get_favorite_by_user(session['user_id'])
        recipes = []
        if fav_recipes:
            for fav_recipe in fav_recipes:
                recipe = crud.get_recipe_by_id(fav_recipe.recipe_id)
                if search_fav.lower() in recipe.recipe_name.lower():
                    recipes.append(recipe)
                    #recipes.append({'recipe_id': recipe.recipe_id, 'recipe_api_id': recipe.recipe_api_id, 'recipe_image': recipe.image, 'recipe_ingredients': recipe.ingredients, 'recipe_name': recipe.recipe_name})
            #return jsonify(recipes)
    return render_template('favorite_recipe.html', user_id=session['user_id'], user_name=session['user_name'], recipes=recipes)

@app.route('/add_to_favorite/<recipe_id>')
def add_to_favorite_recipes(recipe_id):
    """add to favorite recipes"""
    if crud.get_favorite_by_recipe(recipe_id):
        flash("This favorite recipe already exists")
    else:
        fav = crud.create_favorite(session['user_id'], recipe_id)
        db.session.add(fav)
        db.session.commit()
        flash("Added to favorites")
    return redirect('/favorites')

@app.route('/delete_from_favorite/<recipe_id>')
def delete_from_favorite_recipes(recipe_id):
    """delete from favorite recipes"""
    crud.delete_favorite_by_recipeid(recipe_id)
    return redirect('/favorites')
    
@app.route("/shoppinglist")
def get_shopping_list():
    """View shoppinglist."""
    shopping_list = crud.get_shoppinglist_by_user(session['user_id'])
    items = crud.get_items(shopping_list.shoppinglist_id)
    return render_template("shoppinglist.html", user_id=session['user_id'], items=items)

@app.route("/add_to_shoppinglist", methods=['POST'])
def add_to_shopping_list():
    """Add to shopping list"""
    items = request.form.getlist('ingredient')
    shoppinglist = crud.get_shoppinglist_by_user(session['user_id'])
    if not shoppinglist:
        new_shoppinglist = crud.create_shoppinglist(session['user_id'])
        db.session.add(new_shoppinglist)
        db.session.commit()
    added_items_list = []
    if crud.get_items(shoppinglist.shoppinglist_id):
        added_items = crud.get_items(shoppinglist.shoppinglist_id)
        for added_item in added_items:
            added_items_list.append(added_item.item)

    for item in items:
        if item not in added_items_list:
            shoppinglist_item = crud.create_item(shoppinglist.shoppinglist_id, item)
            db.session.add(shoppinglist_item)
            db.session.commit()
        else:
            flash("You have already added this")
    return redirect("/shoppinglist")

@app.route("/delete_item/<item_id>", methods=['POST'])
def delete_item(item_id):
    """Delete item"""
    crud.delete_item(item_id)
    return redirect("/shoppinglist")

@app.route("/update_item/<item_id>", methods=['POST'])
def update_item(item_id):
    """Update item"""
    
    input_item_id = 'edit_grocery'+item_id
    update_item = request.form.get(input_item_id)
    crud.update_item(item_id, update_item)
    
    return redirect("/shoppinglist")

@app.route("/map")
def view_stores_map():
    """Show map of stores."""
    user = crud.get_user_by_id(session['user_id'])
    return render_template("map_stores.html", user=user, user_id=session['user_id'])


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)