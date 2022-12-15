"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb magicingredients")
os.system("createdb magicingredients")

model.connect_to_db(server.app)
model.db.create_all()

# Load recipes data from JSON file
with open("data/recipes.json") as f:
    recipe_data = json.loads(f.read())

# Create recipes, store them in list so we can use them
recipe_in_db = []
for recipe in recipe_data:
    ingred = []
    for item in recipe["extendedIngredients"]:
        ingred.append(item["original"])
    ingreds = ", ".join(ingred)
    recipe_api_id, recipe_name, ingredients, image, steps, total_cook_time = (
        recipe["id"],
        recipe["title"],
        ingreds,
        recipe["image"],
        recipe["instructions"],
        recipe["cookingMinutes"]
    )
   
    db_recipe = crud.create_recipe(recipe_api_id, recipe_name, ingredients, image, steps, total_cook_time)
    recipe_in_db.append(db_recipe)

model.db.session.add_all(recipe_in_db)
model.db.session.commit()

# Create 10 users
for n in range(10):
    username = f"user{n}"
    email = f"user{n}@test.com"  
    password = "test"

    user = crud.create_user(username, email, password)
    model.db.session.add(user)

model.db.session.commit()
