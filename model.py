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

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username} email={self.email}>'

class Recipe(db.Model):
    """A searched recipe."""    
    
    __tablename__ = "recipes"
    
    recipe_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    recipe_api_id = db.Column(db.Integer, nullable=False, unique=True)
    recipe_name = db.Column(db.String)
    ingredients = db.Column(db.String)
    image = db.Column(db.String)
    steps = db.Column(db.Text)
    total_cook_time = db.Column(db.String)
    
    def __repr__(self):
        return f'<Recipe recipe_id={self.recipe_id} recipe_api_id={self.recipe_api_id} recipe_name={self.recipe_name} ingredients={self.ingredients} steps={self.steps}>'
    
class Favorite(db.Model):
    """Saved to favorite recipe."""    
    
    __tablename__ = "favorites"
    
    fav_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.recipe_id"), nullable=False)
    
    user = db.relationship("User", backref="favorites")
    recipe = db.relationship("Recipe", backref="favorites")

    # def __repr__(self):
    #     return f'<Favorite fav_id={self.fav_id}>'

class Shoppinglist(db.Model):
    """A shopping list."""    
    
    __tablename__ = "shoppinglists"
    
    shoppinglist_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    add_date = db.Column(db.DateTime)
    
    user = db.relationship("User", backref="shoppinglists")

    def __repr__(self):
        return f'<Shoppinglist shoppinglist_id={self.shoppinglist_id} add_date={self.add_date}>'

class Item(db.Model):
    """A shopping list item."""    
    
    __tablename__ = "items"
    
    item_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    shoppinglist_id = db.Column(db.Integer, db.ForeignKey("shoppinglists.shoppinglist_id"), nullable=False)
    item = db.Column(db.String)
    amount = db.Column(db.String)
    is_checked = db.Column(db.Boolean)
    
    shoppinglist = db.relationship("Shoppinglist", backref="items")
    
    def __repr__(self):
        return f'<Item item_id={self.item_id} item={self.item} amount={self.amount} is_checked={self.is_checked}>'
    
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


