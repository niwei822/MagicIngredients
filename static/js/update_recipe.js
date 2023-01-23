function updateRecipe(recipe_id) {
    var instructions = document.querySelector('.steps').innerText
    var ingredients = document.querySelector('.ingredients-list').innerText;
    document.querySelector(".steps").remove();
    document.querySelector('.ingredients-list').remove();
    document.querySelector("#edit_recipe").hidden = "hidden";
    document.querySelector('#save-sl').hidden = "hidden";
    document.querySelector("#new_recipe_area").insertAdjacentHTML('beforeend', `
    <div id="update_content" class="container" text-center>
    <form id="edit_fav_recipe" data-recipe-id= "${recipe_id}" action="/edit_fav_recipe/${recipe_id}" method="POST">
    <div class="row">
    <div class="col-6"><textarea id="new_ingredients" name="edit_ingredients" class="input_area" type="text" style="width:80%; height: 400px; margin-left: 40px">${ingredients}</textarea></div>
    <div class="col-6"><textarea id="new_steps" name="edit_steps" class="input_area" type="text" style="width:80%; height: 400px; margin-left: 40px">${instructions}</textarea></div>
    <div class="text-center mb-4"><button id="save_update" style="color: #F4E9CD; background-color: #468189; border-radius: 5px">Save</button></div> 
    </div>
    </form>
    </div>`);
}
