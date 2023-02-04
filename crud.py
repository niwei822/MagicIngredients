"""CRUD operations."""
from model import db, User, Recipe, Favorite, Shoppinglist, Item, connect_to_db
"""User CRUD operations."""

def create_user(username, email, password):
    """Create a new user and return the instance."""
    user = User(username=username, email=email, password=password)
    return user

def get_users():
    """Return a list of all users."""
    return User.query.all()

def get_user_by_id(user_id):
    """Return the user with the given id, or None if not found."""
    return User.query.get(user_id)

def get_user_by_username(username):
    """Return the user with the given username, or None if not found."""
    return User.query.filter(User.username == username).first()

def get_user_by_email(email):
    """Return the user with the given email, or None if not found."""
    return User.query.filter(User.email == email).first()

"""Recipe CRUD operations."""

def create_recipe(recipe_api_id, recipe_name, ingredients, image, steps, total_cook_time,  source_url):
    """Create and return a new recipe."""
    recipe = Recipe(
        recipe_api_id=recipe_api_id,
        recipe_name=recipe_name,
        ingredients=ingredients,
        image=image,
        steps=steps,
        total_cook_time=total_cook_time,
        source_url=source_url
    )
    return recipe

def update_fav_recipe(recipe_id, new_steps, new_ingredients):
    """ Update a favorite recipe given recipe_id and the updated information. """
    recipe = Recipe.query.filter(Recipe.recipe_id == recipe_id).first()
    recipe.ingredients = new_ingredients
    recipe.steps = new_steps
    db.session.commit()

def get_recipes():
    """Return all recipes."""
    return Recipe.query.all()

def get_recipe_by_id(recipe_id):
    """Return a recipe by primary key(id)."""
    return Recipe.query.get(recipe_id)

def get_recipe_by_api_id(recipe_api_id):
    """Return a recipe by Spoonacular recipe id."""
    return Recipe.query.filter_by(recipe_api_id=recipe_api_id).first()

def create_favorite(user_id, recipe_id):
    """Create and return a favorite."""
    fav = Favorite(user_id=user_id, recipe_id=recipe_id)
    return fav

def get_favorite_by_user(user_id):
    """Return all favorite recipes by user."""
    return Favorite.query.filter(Favorite.user_id == user_id).all()

def get_favorite_by_recipe(recipe_id):
    """Return a favorite recipe by recipe_id."""
    return Favorite.query.filter_by(recipe_id=recipe_id).first()

def delete_favorite_by_recipeid(recipe_id):
    """Delete a recipe from favorites"""
    favorite = Favorite.query.filter(Favorite.recipe_id == recipe_id).first()
    db.session.delete(favorite)
    db.session.commit()

"""Shoppinglist CRUD operations."""

def create_shoppinglist(user_id):
    """Create and return a new shoppinglist."""
    return Shoppinglist(user_id=user_id)

def get_shoppinglist_by_user(user_id):
    """Return shoppinglist for a user."""
    return Shoppinglist.query.filter(Shoppinglist.user_id == user_id).first()

"""item CRUD operations."""

def create_item(shoppinglist_id, item):
    """Create and return a new shoppinglist item."""
    return Item(shoppinglist_id=shoppinglist_id, item=item)

def get_items(shoppinglist_id):
    """Return all shoppinglist items."""
    return Item.query.filter(Item.shoppinglist_id == shoppinglist_id).all()

def get_item_by_id(item_id):
    """Return an item by primary key."""
    return Item.query.get(item_id)

def update_item(item_id, new_item):
    """ Update a shoppinglist item given item_id and the updated information. """
    item_update = Item.query.filter(Item.item_id == item_id).first()
    item_update.item = new_item
    db.session.commit()
    
def delete_item(item_id):
    """Delete a shopplinglist item"""
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
