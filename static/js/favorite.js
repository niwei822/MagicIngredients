
function clickedFav(favBtn) {
    const recipeId = favBtn.getAttribute('data-item-id');
    favBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (favBtn.style.color == "grey") { 
        fetch(`/add_to_favorite/${recipeId}`, {
            method: 'POST',
            headers: { "Content-Type": "application/json" }
        })
            .then((response) => response.json())
            .then(() => {
                favBtn.style.color = "red";
                // var editbtn = '<button id="edit_recipe" onclick="updateRecipe(' + recipeId + ')>Edit this recipe</button>';
                // document.querySelector("#instructions").insertAdjacentHTML('beforeend', editbtn);
            });
        }
        else {
            fetch(`/unfavorite/${recipeId}`, {
                method: 'DELETE',
                headers: { "Content-Type": "application/json" }
            })
                .then((response) => response.json())
                .then(() => {
                    favBtn.style.color = "grey";
                });
        }
    });
}

document.querySelectorAll('#heart').forEach((e) => clickedFav(e));