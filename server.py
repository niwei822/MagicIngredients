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

# API keys and URLs for spoonacular and Yelp APIs
API_KEY_SPOONACULAR = os.environ['SPOONACULAR_APIKEY']
API_KEY_YELP = os.environ['YELP_APIKEY']
URL_SPOONACULAR = 'https://api.spoonacular.com/recipes'
URL_YELP = 'https://api.yelp.com/v3/businesses/search'
HEADERS_SPOONACULAR = {"Content-Type": "application/json"}
HEADERS_YELP = {
    "accept": "application/json",
    "Authorization":  'Bearer %s' % API_KEY_YELP}

@app.route("/")
def homepage():
    """View homepage."""
    return render_template("homepage.html")

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user and store their information in the session."""
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    user_name = crud.get_user_by_username(username)
    if user or user_name:
        flash("Email/username already exists. Try again")
        return redirect("/")
    
    user = crud.create_user(username, email, password)
    db.session.add(user)
    db.session.commit()
    session["user_email"] = user.email
    session["user_id"] = user.user_id
    session["user_name"] = user.username
    flash(f"Welcome, {user.username}!")
      
    return redirect(f"/user_home/{user.user_id}")

@app.route("/login", methods=["GET", "POST"])
def login_user():
    """Login user."""
    if request.method == "GET":
        return redirect("/")
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if user and user.password == password:
        session["user_email"] = user.email
        session["user_id"] = user.user_id
        session["user_name"] = user.username
        flash(f"Welcome back. {user.username}!")
        return redirect(f"/user_home/{session['user_id']}")
    flash("Wrong email or password.")
    
    return redirect("/")
        
@app.route("/logout")
def logout_user():
    """Logout user by deleting session information."""
    session.clear()
    return redirect("/")

@app.route('/user_home/<user_id>')
def user_profile(user_id):
    """
    Show the User's homepage after login
    Retrieves user information and 9 random recipes.
    """
    user = crud.get_user_by_id(user_id)
    recipes = retrieve_random_recipes()

    return render_template('user_home.html', user=user, user_id=session['user_id'], recipes=recipes)

def retrieve_random_recipes():
    """
    Retrieve 9 random recipes from the API.
    """
    endpoint = '/random'
    final_url = URL_SPOONACULAR + endpoint
    data = {"number":"9", "apiKey": API_KEY_SPOONACULAR}
    response = requests.get(final_url, headers=HEADERS_SPOONACULAR, params=data).json()
    return response['recipes']

@app.route('/search', methods=["POST"])
def search_recipes():
    """search recipes based on ingredients"""
    ingredients = request.form.get("search").replace(",", ",+")
    recipes = retrieve_recipes_by_ingredients(ingredients)

    if not recipes:
        flash("No rescipe found") 
        return render_template('recipe_results.html', user_id=session['user_id'], recipes=[])    
    return render_template('recipe_results.html', user_id=session['user_id'], recipes=recipes)
 
def retrieve_recipes_by_ingredients(ingredients):
    """
    Retrieve recipes based on ingredients from the API.
    """
    endpoint = '/findByIngredients'
    final_url = URL_SPOONACULAR + endpoint
    data = {"ingredients": ingredients, "apiKey": API_KEY_SPOONACULAR}
    response = requests.get(final_url, headers=HEADERS_SPOONACULAR, params=data).json()
    return response
    
def get_api_recipe(recipe_id):
    """Get the recipe from API"""
    endpoint = f"/{recipe_id}/information"
    final_url = URL_SPOONACULAR + endpoint
    data = {"includeNutrition":"false", "apiKey": API_KEY_SPOONACULAR}
    response = requests.get(final_url, headers=HEADERS_SPOONACULAR, params=data).json()
    return response
    
@app .route('/recipe')
def show_recipe_detail():
    """Display recipe detail when click the recipe name."""
    recipe_id = request.args['id']
    response = get_api_recipe(recipe_id)
    cook_time = response['readyInMinutes']
    recipe_title = response['title']
    recipe_image = response.get('image', None)
    source_name = response['sourceName']
    source_url = response['sourceUrl']
    ingredient_list = response['extendedIngredients']
    ingredients = []
    recipe_ingredient = ""
    for ingredient in ingredient_list:
        ingredients.append(ingredient['original'])
    recipe_ingredient = "**".join(ingredients)
    
    analyzed_instructions = response['analyzedInstructions']
    if not analyzed_instructions:
        steps = [f"Read the detailed instructions on {source_name}"]
        recipe_steps = steps
    else:
        instructions = analyzed_instructions[0]['steps']
        steps = []
        for step in instructions:
            steps.append(step['step'])
        recipe_steps = "**".join(steps)
    
    local_recipe = crud.get_recipe_by_api_id(recipe_id)
    if not local_recipe:
        new_recipe = crud.create_recipe(recipe_id, recipe_title, recipe_ingredient, recipe_image, recipe_steps, cook_time, source_url)
        db.session.add(new_recipe)
        db.session.commit()
    local_recipe = crud.get_recipe_by_api_id(recipe_id)
    is_in_favorite = is_favorite(local_recipe.recipe_id)
    return render_template('recipe_detail.html', is_in_favorite=is_in_favorite, user_id=session['user_id'], recipe=response, cook_time=cook_time, source_url=source_url, recipe_title=recipe_title, recipe_image=recipe_image,ingredients=ingredients, steps=steps, local_recipe_id=local_recipe.recipe_id)

@app .route('/recipe_fav')
def show_fav_recipe_detail():
    """Display favorite recipe detail when click the recipe name."""
    recipe_id = request.args['id']
    local_recipe = crud.get_recipe_by_id(recipe_id)
    
    source_url = local_recipe.source_url
    is_in_favorite = is_favorite(local_recipe.recipe_id)
    cook_time = local_recipe.total_cook_time
    recipe_title = local_recipe.recipe_name
    ingredients = local_recipe.ingredients.split("**")
    steps = local_recipe.steps.split("**")

    recipe_image = local_recipe.image
    return render_template('recipe_detail.html', is_in_favorite=is_in_favorite, user_id=session['user_id'], recipe=local_recipe, cook_time=cook_time, source_url=source_url, recipe_title=recipe_title, recipe_image=recipe_image, ingredients=ingredients, steps=steps, local_recipe_id=local_recipe.recipe_id)

def is_favorite(recipe_id):
    """Check if the recipe is in the user's favorite list."""
    fav_recipes = crud.get_favorite_by_user(session['user_id'])
    
    for fav_recipe in fav_recipes:
        if recipe_id == fav_recipe.recipe_id:
            return True
    return False

@app.route('/edit_fav_recipe/<recipe_id>', methods=["POST"])
def edit_recipe(recipe_id):
    """edit steps and ingredients in user's fav recipe"""
    updated_instructions = request.form.get("edit_steps").replace("\r\n", "**")
    updated_ingredients = request.form.get("edit_ingredients").replace("\r\n", "**")
    crud.update_fav_recipe(recipe_id, updated_instructions, updated_ingredients)
    flash("Recipe updated!")
    return redirect (f"/recipe_fav?id={recipe_id}")

@app.route('/favorites', methods=["GET", "POST"])
def favorite_recipes():
    """
    Display and search favorite recipes by keyword input
    """
    if request.method == "GET":
        # Get all favorite recipes by user ID
        fav_recipes = crud.get_favorite_by_user(session['user_id'])
        # Create a list to store the recipe objects
        recipes = []
        
        # Loop through the favorite recipes and retrieve the recipe details
        if fav_recipes:
            for fav_recipe in fav_recipes:
                recipe = crud.get_recipe_by_id(fav_recipe.recipe_id)
                recipes.append(recipe) 
    else:
        # Get the keyword to search for in the favorite recipes
        search_fav = request.form.get("search_fav")
        # Get all favorite recipes by user ID
        fav_recipes = crud.get_favorite_by_user(session['user_id'])
        
        recipes = []
        
        if fav_recipes:
            for fav_recipe in fav_recipes:
                recipe = crud.get_recipe_by_id(fav_recipe.recipe_id)
                
                if search_fav.lower() in recipe.recipe_name.lower():
                    recipes.append(recipe)
    return render_template('favorite_recipe.html', user_id=session['user_id'], user_name=session['user_name'], recipes=recipes)

@app.route('/add_to_favorite/<recipe_id>', methods=["POST"])
def add_to_favorite_recipes(recipe_id):
    """add to favorite recipes"""
    fav = crud.create_favorite(session['user_id'], recipe_id)
    
    db.session.add(fav)
    db.session.commit()
    
    response = {"success":True}
    return jsonify(response)

@app.route('/unfavorite/<recipe_id>', methods=['DELETE'])
def unfavorite_recipe(recipe_id):
    """remove from favorite recipes"""
    
    crud.delete_favorite_by_recipeid(recipe_id)
    response = {"success":True}
    return jsonify(response)

@app.route('/delete_from_favorite/<recipe_id>')
def delete_from_favorite_recipes(recipe_id):
    """delete from favorite recipes"""
    crud.delete_favorite_by_recipeid(recipe_id)
    return redirect('/favorites')
    
@app.route("/shoppinglist")
def get_shopping_list():
    """View shoppinglist."""
    user_id = session['user_id']
    shopping_list = crud.get_shoppinglist_by_user(user_id)
    if shopping_list:
        items = crud.get_items(shopping_list.shoppinglist_id)
    else:
        items = []
    return render_template("shoppinglist.html", user_id=user_id, items=items)

@app.route("/add_to_shoppinglist", methods=['POST'])
def add_item_to_shopping_list():
    """Add to shopping list"""
    items = request.form.getlist('ingredient')
    shoppinglist = crud.get_shoppinglist_by_user(session['user_id'])
    if not shoppinglist:
        new_shoppinglist = crud.create_shoppinglist(session['user_id'])
        db.session.add(new_shoppinglist)
        db.session.commit()
        shoppinglist = crud.get_shoppinglist_by_user(session['user_id'])
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

@app.route("/delete_item/<item_id>", methods=['DELETE'])
def delete_item(item_id):
    """Delete item"""
    crud.delete_item(item_id)
    response = {"success":True}
    return jsonify(response)

@app.route("/update_item/<item_id>", methods=['POST'])
def update_item(item_id):
    """Update item"""
    update_item = request.json.get("name")
    crud.update_item(item_id, update_item)
    response = {"success":True} 
    return jsonify(response)

@app.route("/map")
def view_stores_map():
    """Show map of stores."""
    user = crud.get_user_by_id(session['user_id'])
    return render_template("map_stores.html", user=user, user_id=session['user_id'])

@app.route('/search_restaurant/<recipe_id>', methods=["POST"])
def search_restaurant(recipe_id):
    """search restaurant based on input"""
    recipe  = crud.get_recipe_by_id(recipe_id)
    location = request.form.get("search_rest")
    data = {"location": location, "term": recipe.recipe_name, "open_now": True, "sort_by": "rating",}
    response = requests.get(URL_YELP, headers=HEADERS_YELP, params=data).json()
    if not response:
        flash("No restaurant found") 
        return render_template('search_restaurant.html', restaurants=response)
    
    return render_template('search_restaurant.html', user_id=session['user_id'], recipe_id=recipe_id, recipe_name=recipe.recipe_name, restaurants=response["businesses"])

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)