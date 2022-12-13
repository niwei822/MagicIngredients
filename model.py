"""Models for recipe searching app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    # recipes = db.relationship("Recipe", back_populates="user")
    # favorites = db.relationship("Favorite", back_populates="user")
    # shoppinglists = db.relationship("Shoppinglist", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username} email={self.email}>'

class Recipe(db.Model):
    """A custom recipe."""    
    
    __tablename__ = "recipes"
    
    recipe_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    recipe_name = db.Column(db.Text)
    ingredients_need = db.Column(db.String)
    image = db.Column(db.String)
    steps = db.Column(db.String)
    total_cook_time = db.Column(db.String)
    
    user = db.relationship("User", backref="recipes")
    ingredients = db.relationship("Ingredient", secondary="recipe_ingredients", back_populates="recipes")
    
    def __repr__(self):
        return f'<Recipe recipe_id={self.recipe_id} recipe_name={self.recipe_name} steps={self.steps}>'
    
class Favorite(db.Model):
    """Saved to favorite recipe."""    
    
    __tablename__ = "favorites"
    
    fav_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __repr__(self):
        return f'<Favorite fav_id={self.fav_id}>'

class Shoppinglist(db.Model):
    """A shopping list."""    
    
    __tablename__ = "shoppinglists"
    
    shoppinglist_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    add_date = db.Column(db.DateTime)
    
    user = db.relationship("User", backref="shoppinglists")

    def __repr__(self):
        return f'<Shoppinglist shoppinglist_id={self.shoppinglist_id} add_date={self.add_date}>'

class Ingredient(db.Model):
     """An ingredient."""
     __tablename__ = "ingredients"
     
     ingredient_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
     ingredient_name = db.Column(db.String)
     
     recipes = db.relationship("Recipe", secondary="recipe_ingredients", back_populates="ingredients")
     
     def __repr__(self):
        return f'<Ingredient ingredient_id={self.ingredient_id} ingredient_name={self.ingredient_name}>'
     

class Item(db.Model):
    """A shopping list item."""    
    
    __tablename__ = "items"
    
    item_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.ingredient_id"))
    shoppinglist_id = db.Column(db.Integer, db.ForeignKey("shoppinglists.shoppinglist_id"))
    ingredients = db.Column(db.String)
    amount = db.Column(db.String)
    is_checked = db.Column(db.Boolean)
    
    shoppinglist = db.relationship("Shoppinglist", backref="items")
    
    def __repr__(self):
        return f'<Recipe recipe_id={self.recipe_id} recipe_name={self.recipe_name} steps={self.steps}>'

class RecipeIngredient(db.Model):
    """“glue between recipes and ingredients."""

    __tablename__ = "recipe_ingredients"

    recipe_ingredient_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"))
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.ingredient_id"))
    
def connect_to_db(flask_app, db_uri="postgresql:///magicingredients", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    #from server import app
    from flask import Flask

    app = Flask(__name__)
    connect_to_db(app)
    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.


