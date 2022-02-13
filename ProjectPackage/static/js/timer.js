// console.log(1)
window.onload=update_timer();
function update_timer(){
    var innerhour=document.getElementById("hour");
    var innerminutes=document.getElementById("minutes");
    var innersec=document.getElementById("sec");
    today=new Date();
    hour=String(today.getHours());
    minutes=String(today.getMinutes());
    sec=String(today.getSeconds());
    if (hour<10)
        hour="0"+hour;
    if (minutes<10)
        minutes="0"+minutes;
    if (sec<10)
        sec="0"+sec;
    innerhour.innerText=hour;
    innerminutes.innerText=minutes;
    innersec.innerText=sec;
    setTimeout("update_timer()",1000);
}
