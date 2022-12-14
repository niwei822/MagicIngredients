"""CRUD operations."""

from model import db, User, Recipe, Favorite, Shoppinglist, Item, connect_to_db

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


def get_recipes():
    """Return all recipes."""

    return Recipe.query.all()


def get_recipe_by_id(recipe_id):
    """Return a recipe by primary key."""

    return Recipe.query.get(recipe_id)

def get_recipe_by_api_id(recipe_api_id):
    """Return a recipe by Spoonacular recipe id."""

    return Recipe.query.filter_by(recipe_api_id=recipe_api_id).first()

def create_favorite(user_id, recipe_id):
    """Create and return a new rating."""

    fav = Favorite(user_id=user_id, recipe_id=recipe_id)

    return fav




def create_rating(user, movie, score):
    """Create and return a new rating."""

    rating = Rating(user=user, movie=movie, score=score)

    return rating


def update_rating(rating_id, new_score):
    """ Update a rating given rating_id and the updated score. """
    rating = Rating.query.get(rating_id)
    rating.score = new_score

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
