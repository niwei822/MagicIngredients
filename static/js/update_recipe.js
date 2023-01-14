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
    <div class="col-6"><textarea id="new_steps" name="edit_steps" class="input_area" type="text" style="width:80%; height: 400px; margin-left: 40px">${instructions}</textarea></div>
    <div class="col-6"><textarea id="new_ingredients" name="edit_ingredients" class="input_area" type="text" style="width:80%; height: 400px; margin-left: 40px">${ingredients}</textarea></div>
    <p style="margin-left: 40px; margin-top: 20px"><button class="text-center" id="save_update">Save</button></p> 
    </div>
    </form>
    </div>`);
}
//     function saveUpdatedRecipe() {
//         var updateInstructions = document.querySelector("#new_steps")
//         var updateIngredients = document.querySelector("#new_ingredients")
//         var recipeId = document.getElementById("edit_fav_recipe").getAttribute('data-recipe-id')
//         if (updateInstructions.value == "" || updateIngredients == "") {
//             alert("Please write something!");
//         }
//         else {
//             document.getElementById("update_content").remove();
//             querySelector(".recipe_steps").insertAdjacentHTML('beforeend',`
//             <ol class="steps">
//             {% if steps is string %}
//             <li> {{steps}} </li>
//             <li><a class="source_url" href="{{source_url}}">Link To The Original Recipe</Source></a> </li>
//             {% else %}
//             {% for step in steps %}
//             <li>
//                 {{ step }}
//             </li>
//             {% endfor %}
//             {% endif %}
//         </ol>`
//             );
//     }
// }
// }
