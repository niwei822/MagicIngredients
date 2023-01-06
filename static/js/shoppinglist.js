
function check_clicked(item_id){
  ItemId = item_id;
  var checked_input = document.querySelector("[id='"+item_id+"']");
  const checked_label = document.querySelector("[data-input-id='"+item_id+"']");
  if (checked_input.checked) {
    checked_label.style.textDecoration = "line-through";
    checked_label.style.color = "#01A88A";
    var add_html = '<button type="submit" class="trash" id="trash'+item_id+'" data-item-id='+item_id+'>🗑️</button>'
    document.querySelector("[data-input-id='"+item_id+"']").insertAdjacentHTML('afterend', add_html);
  }
  else {
    checked_label.style.textDecoration = "";
    document.getElementById("trash"+item_id).style.display = "none"
  }

function delete_clicked(delete_btn){
  const ItemId = delete_btn.getAttribute('data-item-id');
  delete_btn.addEventListener('click', () => { 
    fetch(`/delete_item/${ItemId}`, {
      method: 'DELETE',
      headers: {"Content-Type":"application/json"}
    })
      .then((response) => response.json())
      .then(() => {
        delete_btn.parentElement.remove();
      });
    });
}
  
document.querySelectorAll("#trash"+ItemId).forEach((e) => delete_clicked(e));
  

  // const btn = document.getElementById("remove_grocery");
  // btn.value = "Delete items";
  // btn.style.color = "#01A88A";
  // btn.backgroundColor = "#FE7575";
  // if (checked_input.checked == false) {
  //   btn.value = "Check items";
  //   btn.style.color = "BLACK";
  //   btn.backgroundColor = "WHITE";
  //   checked_label.style.color = "BLACK";
  // }
}

function edit_grocery(item_id){
  var item_name = document.querySelector("[data-input-id='"+item_id+"']").innerHTML.replace(/ /g, '\xa0');
  console.log(item_name)
  var add_html = '<div><form action="/update_item/'+item_id+'" method="POST"><input name="edit_grocery'+item_id+'" class="input_area" type="text" value='+item_name+'><input type="submit"></form></div>'
  document.querySelector("[data-input-id='"+item_id+"']").insertAdjacentHTML('beforebegin', add_html);
  document.querySelector("[data-input-id='"+item_id+"']").style.display = "none";
  // var grocery_text = document.getElementById("grocery_input");
  // grocery_text.value = item_name;
}

function newItem() {
  var add_btn = document.querySelector("[id='grocery']");
  var inputValue = document.getElementById("grocery_input").value;
  if (inputValue === '') {
      alert("Please write something first!");
      add_btn.disabled = true;
  }
}

function enable() {
  var add_btn = document.querySelector("[id='grocery']");
  var inputValue = document.getElementById("grocery_input").value;
  if (inputValue != '') {
      add_btn.disabled = false;
  }
}

