"""CRUD operations."""

from model import db, User, Recipe, Favorite, Shoppinglist, Item, connect_to_db
from datetime import datetime
"""User CRUD operations."""

def create_user(username, email, password):
    """Create and return a new user."""

    user = User(username=username,email=email, password=password)

    return user

def get_users():
    """Return all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

def get_user_by_username(username):
    """Return a user by username."""
    
    return User.query.filter(User.username == username).first()

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

"""Recipe CRUD operations."""

def create_recipe(recipe_api_id, recipe_name, ingredients, image, steps, total_cook_time):
    """Create and return a new recipe."""

    recipe = Recipe(
        recipe_api_id=recipe_api_id,
        recipe_name=recipe_name,
        ingredients=ingredients,
        image=image,
        steps=steps,
        total_cook_time=total_cook_time
    )

    return recipe

def update_fav_recipe(recipe_id, recipe_api_id, recipe_name, new_ingredients, image, new_steps, total_cook_time):
    """ Update a favorite recipe given recipe_id and the updated information. """
    
    recipe_update = Recipe.query.filter(Recipe.recipe_id==recipe_id).first()
    recipe_update.recipe_api_id = recipe_api_id
    recipe_update.recipe_name = recipe_name
    recipe_update.ingredients = new_ingredients
    recipe_update.image = image
    recipe_update.steps = new_steps
    recipe_update.total_cook_time = total_cook_time
    db.session.commit()
    return

def get_recipes():
    """Return all recipes."""

    return Recipe.query.all()

def get_recipe_by_id(recipe_id):
    """Return a recipe by primary key."""

    return Recipe.query.get(recipe_id)

def get_recipe_by_api_id(recipe_api_id):
    """Return a recipe by Spoonacular recipe id."""

    return Recipe.query.filter_by(recipe_api_id=recipe_api_id).first()
#not sure need this?
def create_favorite(user_id, recipe_id):
    """Create and return a favorite."""

    fav = Favorite(user_id=user_id, recipe_id=recipe_id)

    return fav

def get_favorite_by_user(user_id):
     """Return all favorite recipes by user."""
     
     return Favorite.query.filter(Favorite.user_id==user_id).all()
 
def get_favorite_by_recipe(recipe_id):
    """Return a favorite recipe by recipe_id."""
    
    return Favorite.query.filter_by(recipe_id=recipe_id).first()

def delete_favorite_by_recipeid(recipe_id):
    """Delete a recipe from favorites"""
    
    recipe = Favorite.query.filter(Favorite.recipe_id == recipe_id).first()
    db.session.delete(recipe)
    db.session.commit()

"""Shoppinglist CRUD operations."""

def create_shoppinglist(user_id):
    """Create and return a new shoppinglist."""

    shoppinglist = Shoppinglist(user_id=user_id, add_date=datetime.now())

    return shoppinglist

def get_shoppinglist_by_user(user_id):
     """Return all favorite recipes by user."""
     
     return Shoppinglist.query.filter(Shoppinglist.user_id==user_id).first()

"""item CRUD operations."""

def create_item(shoppinglist_id, item, amount=0, is_checked=0):
    """Create and return a new shoppinglist item."""

    item = Item(
        shoppinglist_id=shoppinglist_id,
        item=item,
        amount=amount,
        is_checked=is_checked,
    )

    return item

def get_items(shoppinglist_id):
    """Return all shoppinglist items."""

    return Item.query.filter(Item.shoppinglist_id==shoppinglist_id).all()

def get_item_by_id(item_id):
    """Return an item by primary key."""

    return Item.query.get(item_id)

def update_item(item_id, new_item, amount=0, is_checked=0):
    """ Update a shoppinglist item given item_id and the updated information. """
    
    item_update = Item.query.filter(Item.item_id==item_id).first()
    item_update.item = new_item
    item_update.amount = amount
    item_update.is_checked = is_checked
    db.session.commit()
    return

def delete_item(item_id):
    """Delete a shopplinglist item"""
    
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
