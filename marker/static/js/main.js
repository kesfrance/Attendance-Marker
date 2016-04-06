
function Hide(target){
  document.getElementById(target).style.display= "none";
}
	
function Show(target){
  document.getElementById(target).style.display= "block";
}

function deleteItem(val, valid){
  var ans = confirm('Sure You Deleting: '+ val);
  if (ans) {
    document.getElementById('deleteitem').value = valid;
    document.getElementById('form2').submit();
	}
 }


