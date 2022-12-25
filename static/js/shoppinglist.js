function check_clicked(input_id){
  var checked_input = document.querySelector("[id='"+input_id+"']");
  const checked_label = document.querySelector("[for='"+input_id+"']");
  if (checked_input.checked) {
    checked_label.style.textDecoration = "line-through";
    checked_label.style.color = "#01A88A";
  }
  else {
    checked_label.style.textDecoration = "";
  }
  
  const btn = document.getElementById("remove_grocery");
  btn.value = "Delete items";
  btn.style.color = "#01A88A";
  btn.backgroundColor = "#FE7575";
  if (checked_input.checked == false) {
    btn.value = "Check items";
    btn.style.color = "BLACK";
    btn.backgroundColor = "WHITE";
    checked_label.style.color = "BLACK";
}
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