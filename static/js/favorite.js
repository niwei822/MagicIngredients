
function clickedFav(favBtn) {
    const recipeId = favBtn.getAttribute('data-item-id');
    favBtn.addEventListener('click', () => {
        if (favBtn.style.color == "grey") { 
        fetch(`/add_to_favorite/${recipeId}`, {
            method: 'POST',
            headers: { "Content-Type": "application/json" }
        })
            .then((response) => response.json())
            .then(() => {
                favBtn.style.color = "red";
            });
        }
        else {
            fetch(`/unfavorite/${recipeId}`, {
                method: 'DELETE',
                headers: { "Content-Type": "application/json" }
            })
                .then((response) => response.json())
                .then(() => {
                    favBtn.style.color = "gray";
                });
        }
    });
}

document.querySelectorAll('#heart').forEach((e) => clickedFav(e));