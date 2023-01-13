function updateRecipe() {
    var instructions = document.querySelector('.steps').innerText
    console.log(instructions)
    var stepsInput = '<textarea id="new_steps" name="edit_steps" class="input_area" type="text" style="width:85%; height: 400px; margin-left: 20px">' + instructions + '</textarea>'
    document.querySelector(".steps").insertAdjacentHTML('beforebegin', stepsInput);
    document.querySelector(".steps").remove();

}
document.querySelector('#edit_recipe').addEventListener('click', updateRecipe);


