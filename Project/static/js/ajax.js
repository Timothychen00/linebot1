
function change_options(){
    key_v=document.getElementById('key').value
    value_v=document.getElementById('value').value;
    console.log(value);
    xhr=new XMLHttpRequest();
    xhr.onload = function(e) {
        document.getElementById('state').value=xhr.response;
    }
    xhr.open('GET','/customers/?key='+key_v+'&value='+value_v+'&type=str',true);
    xhr.send()
}
value=document.getElementById("value");
key=document.getElementById("key");
value.addEventListener("change",change_options);