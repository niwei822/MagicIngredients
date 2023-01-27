# Magic Ingredients
#### A Hackbright capstone project. Magic Ingredients is a full-stack web application allows users to search for delicious recipes within seconds using limited ingredients, in addition to creating a grocery shopping list/locating the nearest grocery store for later completion.

## Table of Contents
- [Background](#background)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Installation](#installation)
- [For Version 2.0](#for-version-20)

## Background
Not sure what to cook with limited ingredients? With this application, the user is able to view random recipes or search for recipes in seconds using what they have at home. The user can save and edit their favorite recipes. Another feature of this website allows users to create grocery shopping lists for later completion if they are missing ingredients for a certain recipe. Users will also be able to locate grocery stores using Google maps. Don't feel like cooking? No problem at all! Users can also search for restaurants with the most popular menu that matches a particular recipe. 

## Tech Stack
- Backend: Python3, Flask framework, SQLAlchemy ORM, Postgresql database
- Frontend: HTML, CSS, JavaScript, AJAX, JSON, Jinja2, Bootstrap5
- API: Spoonacular API, Google Places API, Yelp Fusion API

## Features
### Login and Create New Account
![ezgif com-gif-maker](https://user-images.githubusercontent.com/69645683/215015329-895ff4a8-0ea6-4e72-9b3f-427e22fd7051.gif)
### View Random Recipes and Search Recipes by Ingredients
- Users are presented with a home page with random recipes displayed in carousels once they have logged in.
![random](https://user-images.githubusercontent.com/69645683/215016454-9c31fe0f-db2b-41d4-8032-bdd47fa545ef.gif)
- By entering ingredients, users are able to search for recipes.
![search ingredients](https://user-images.githubusercontent.com/69645683/215016786-f405fd36-cbbc-4ac6-9cb8-24cbe1a7f79b.gif)
### Favorites
- Upon clicking the recipe name, users can toggle the heart button to favorite/unfavorite the recipe.
![favor:unfavor](https://user-images.githubusercontent.com/69645683/215017949-9aea9e70-1c29-4c70-b3c8-132c6ebbce10.gif)
- Users may also remove a recipe from their favorites or search for a recipe by entering keywords under the favorites tab.
![search fav](https://user-images.githubusercontent.com/69645683/215018110-a4aa3c8a-53f5-4bf2-bced-03a73ee8f9cc.gif)
### Edit recipe
- The user has the option of editing the ingredients and instructions of their favorite recipes.
![edit favor](https://user-images.githubusercontent.com/69645683/215018475-834c99e2-c403-4d33-96ab-1138dc786d2d.gif)
### Search for restaurants
- The "don't feel like cooking" button lets users find restaurants with the most popular menus that match a particular recipe.
![search restaurants](https://user-images.githubusercontent.com/69645683/215018892-71c6dfc0-212f-4c43-9747-8c192161cf1e.gif)
### All about shopping list
- The user may add any missing ingredients to the shopping list, as well as their own groceries. In addition, each grocery item can be updated or deleted.
![shoppinglist](https://user-images.githubusercontent.com/69645683/215020233-67ea9c0d-9d71-4c68-8624-8608c20cb0b7.gif)
### Locate grocery stores
- Users can locate nearby grocery stores with the autocomplete feature of the Google Places API. By entering the zip code or city, stores will be found and custom markers will be displayed. Clicking on a marker will display store details in an info window.
![map](https://user-images.githubusercontent.com/69645683/215022047-e625c1e4-fdd1-4137-96d0-8ce89275caed.gif)
## Installation
- Clone or fork this repository:
[Magic Ingredients](https://github.com/niwei822/MagicIngredients)


## For Version 2.0
