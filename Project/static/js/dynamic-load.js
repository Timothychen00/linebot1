
function getScrollTop()
{
    var dashboard=document.getElementById('dashboard');
    var scrollTop = 0, bodyScrollTop = 0, documentScrollTop = 0;
    if(dashboard){
        bodyScrollTop = dashboard.scrollTop;
    }
    if(document.documentElement){
        documentScrollTop = document.documentElement.scrollTop;
    }
scrollTop = (bodyScrollTop - documentScrollTop > 0) ? bodyScrollTop : documentScrollTop;
return scrollTop;
}

function getScrollHeight(){
        var dashboard=document.getElementById('dashboard');
    　　var scrollHeight = 0, bodyScrollHeight = 0, documentScrollHeight = 0;
    　　if(dashboard){
    　　　　bSH = dashboard.scrollHeight;
    　　}
    　　if(document.documentElement){
    　　　　dSH = document.documentElement.scrollHeight;
    　　}
    scrollHeight = (bSH - dSH > 0) ? bSH : dSH ;
    　　return scrollHeight;
    }

function getWindowHeight(){
    var dashboard=document.getElementById('dashboard');
    var windowHeight = 0;
    if(document.compatMode == "CSS1Compat"){
        windowHeight = document.documentElement.clientHeight;
    }else{
        windowHeight = dashboard.clientHeight;
    }
    return windowHeight;
}


function find(type='dynamic',month=null,key_v=null,value_v=null){
    if (key_v==null)
    {
        key_v=document.getElementById('type').value
        value_v=document.getElementById('value').value;
    }
    console.log(value);
    xhr=new XMLHttpRequest();

    var start=1;
    table=document.querySelector("#place tr:last-child td");
    if (table){
        console.log(table.textContent);
        start=table.textContent;
    }
    xhr.onload = function(e) {
        var place=document.getElementById('place');
        //place.innerHTML=a[0]
        a=JSON.parse(xhr.response);

        length=20;
        for (let i=0;i<length;i++){
    
        place.innerHTML+="\
            <tr>\
                <td>"+a[i][0][1]+"</td>\
                <td><a href=\'/customers/"+a[i][0][1]+"/\'>"+a[i][1][1]+"</a></td>\
                <td>\
                    <button type=\"button\" class=\"btn btn-danger\" data-bs-toggle=\"modal\" data-bs-target=\"#exampleModal"+a[i][0][1]+"\">刪除</button>\
                    <div class=\"modal fade\" id=\"exampleModal"+a[i][0][1]+"\" tabindex=\"-1\" aria-labelledby=\"exampleModalLabel\" aria-hidden=\"true\">\
                        <div class=\"modal-dialog\">\
                            <div class=\"modal-content\">\
                                <div class=\"modal-header\">\
                                    <h5 class=\"modal-title\" id=\"exampleModalLabel\">確認刪除？</h5>\
                                    <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"modal\" aria-label=\"Close\"></button>\
                                </div>\
                                <div class=\"modal-body\">\
                                    <p class=\"fw-bold\">請注意！刪除後將無法復原！</p>\
                                </div>\
                                <div class=\"modal-footer\">\
                                    <button type=\"button\" class=\"btn btn-secondary\" data-bs-dismiss=\"modal\">取消</button>\
                                    <button type=\"button\" class=\"btn btn-danger\" onclick=\"location.href=\'/customers/"+a[i][0][1]+"/delete/ \'\" >確認刪除</button>\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                </td>\
            </tr>"
        }
    }
    if  (month==null)
        month='';
    var place=document.getElementById('place');
    if (type=='dynamic')
    {
        xhr.open('GET','/customers/?key='+key_v+'&value='+value_v+"&type=json&start="+start+"&length=20&month="+month,true);
    }else{
        place.innerHTML='';
        xhr.open('GET','/customers/?key='+key_v+'&value='+value_v+"&type=json&month="+month,true);
    }
    xhr.send()
}
var dashboard=document.getElementById('dashboard');
dashboard.onscroll = function(){
    console.log(getScrollTop(),getWindowHeight(),getScrollHeight(),dashboard.offsetHeight);
    if(Math.abs(getScrollTop() - getScrollHeight()+dashboard.offsetHeight)<2){
        find()
    }
};

//dashboard.onload=find();