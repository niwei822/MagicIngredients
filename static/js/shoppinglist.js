
document.querySelector("#add_grocery").addEventListener("submit", (event) => {
    event.preventDefault();
    const grocery_item = document.querySelector('#grocery_input')
    document.querySelector('#add_item').insertAdjacentHTML('beforeend', `<li>${grocery_item}</li>`);
      });
 
