function check_clicked(item_id) {
  var checked_input = document.querySelector("[id=checkbox" + item_id + "]");
  const checked_label = document.querySelector("[data-input-id='" + item_id + "']");
  if (checked_input.checked) {
    checked_label.style.textDecoration = "line-through";
    checked_label.style.color = "#01A88A";
    var add_html = '<button type="submit" class="trash" id="trash' + item_id + '" data-item-id=' + item_id + '>🗑️</button>'
    document.querySelector("[data-input-id='" + item_id + "']").insertAdjacentHTML('afterend', add_html);
  }
  else {
    checked_label.style.textDecoration = "";
    document.getElementById("trash" + item_id).style.display = "none"
  }

  function delete_clicked(delete_btn) {
    delete_btn.addEventListener('click', () => {
      fetch(`/delete_item/${item_id}`, {
        method: 'DELETE',
        headers: { "Content-Type": "application/json" }
      })
        .then((response) => response.json())
        .then(() => {
          delete_btn.parentElement.remove();
        });
    });
  }
  document.querySelectorAll("#trash" + item_id).forEach((e) => delete_clicked(e));
}

function edit_grocery(item_id) {

  var item_name = document.querySelector("[data-input-id='" + item_id + "']").innerHTML.replace(/ /g, '\xa0');
  var add_html = '<div><input data-item-id=' + item_id + ' name="edit_grocery' + item_id + '" class="input_area" type="text" value=' + item_name + '><button id= "sub">Save</button></div>'
  document.querySelector("[data-input-id='" + item_id + "']").insertAdjacentHTML('beforebegin', add_html);
  document.querySelector("[data-input-id='" + item_id + "']").remove();

  function updateItem() {

    var myInput = document.querySelector(".input_area")
    var itemId = myInput.getAttribute('data-item-id')
    console.log(myInput.value)
    console.log(itemId)
    if (myInput.value == "") {
      alert("Please write something!");
    }
    else {
      content = {
        name: myInput.value,
      };
      console.log(JSON.stringify(content))
      fetch(`/update_item/${itemId}`, {
        method: 'POST',
        body: JSON.stringify(content),
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((response) => response.json())
        .then(() => {
          var updateLabel = `<label class="grocery_label" data-input-id=${item_id} name=${item_id} onclick="edit_grocery(${item_id})">${myInput.value}</label>`
          document.querySelector(".input_area").parentElement.remove();
          checkboxid = ".checkbox" + itemId
          document.querySelector("[id='checkbox" + item_id + "']").insertAdjacentHTML('afterend', updateLabel);
        });
    }
  }
  console.log(document.querySelector('#sub'))
  document.querySelector('#sub').addEventListener('click', updateItem);
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

