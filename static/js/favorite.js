
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
                var editbtn = '<div class="col-md-12 text-center"><button id="edit_recipe">Edit this recipe</button></div>'
                document.querySelector("#recipe-content").insertAdjacentHTML('beforeend', editbtn);
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
                    document.querySelector("#edit_recipe").style.display == "none";
                });
        }
    });
}

document.querySelectorAll('#heart').forEach((e) => clickedFav(e));