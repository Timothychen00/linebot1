var page_index=1;
var max_index=10;
var type="";
var t_month=null;

function this_month(){
    window.page_index=1;
    document.getElementById('page_index').innerText=page_index;
    window.t_month="this_month";
    window.type="dynamic";

    value=(page_index-1)*25
    if(value==0)
        value=1;
    find(type,"next-time","1",value);
}

function next_month(){
    window.page_index=1;
    document.getElementById('page_index').innerText=page_index;
    window.t_month="next_month";
    window.type="search";

    value=(page_index-1)*25
    if(value==0)
        value=1;
    find(type,"next-time","1",value);
}
// alert(3);

next_page=()=>{
    window.page_index+=1;
    // let now=document.getElementById('page_index').value;
    let value=null;
    if (t_month)
        value="1";
    // alert(t_month);
    find("dynamic",t_month,value,page_index);
    
    document.getElementById('page_index').innerText=page_index;
}

last_page=()=>{
    if(page_index>1)
        window.page_index-=1;
    
    let value=null;
    if (t_month)
        value="1";
        alert(t_month);
    find("dynamic",t_month,value,page_index);
    document.getElementById('page_index').innerText=page_index;

}

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

var month='';
function find(type='dynamic',key_v=null,value_v=null,start=1){
//    alert(2);
    if (t_month)
        month=t_month
    if (key_v==null)
    {
        key_v=document.getElementById('type').value;
        value_v=document.getElementById('value').value;
    }
    console.log(value);
    xhr=new XMLHttpRequest();
    if(page_index!=1)
    {
        
        start=(page_index-1)*25;
        if(start==0)
            start=1;
        
    }
    // alert(page_index);
    // alert(start);
    // var start=1;
    table=document.querySelector("#place");
    if (table){
        console.log(table.childElementCount);//因爲每一個tr的編號不一定是間隔1，所以要接續之前結果要用childElementCount
        // start=table.childElementCount;
    }
    xhr.onload = function(e) {
        // alert(1);
        var place=document.getElementById('place');
        //place.innerHTML=a[0]
        a=JSON.parse(xhr.response);
        console.log(a);
        var month=a[0];

        a.shift();
        console.log(a[1]);
        length=25;
        place.innerHTML="";
        for (let i=0;i<length;i++){
        // place.innerHTML="";
        place.innerHTML+="\
            <tr>\
                <td>"+a[i][0]+"</td>\
                <td><a href=\'/customers/"+a[i][0]+"/\'>"+a[i][1]+"</a></td>\
                <td>"+a[i][2]+"</td>\
                <td>"+a[i][3]+"</td>\
                <td>\
                    <button type=\"button\" class=\"btn btn-danger\" data-bs-toggle=\"modal\" data-bs-target=\"#exampleModal"+a[i][0]+"\">刪除</button>\
                    <div class=\"modal fade\" id=\"exampleModal"+a[i][0]+"\" tabindex=\"-1\" aria-labelledby=\"exampleModalLabel\" aria-hidden=\"true\">\
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
                                    <button type=\"button\" class=\"btn btn-danger\" onclick=\"location.href=\'/customers/"+a[i][0]+"/delete/ \'\" >確認刪除</button>\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                </td>\
            </tr>"
        }
    }
    // alert(month);
    var place=document.getElementById('place');
    url='';
    if (type=='dynamic')
    {
        if (month==null || month=='none')
            url='/customers/?key='+key_v+'&value='+value_v+"&type=json&start="+start+"&length=25";
        else
            url='/customers/?key='+key_v+'&value='+value_v+"&type=json&start="+start+"&length=25&month="+month;
    }else{
        place.innerHTML='';
        if (month==null || month=='none')
        {
            url='/customers/?key='+key_v+'&value='+value_v+"&type=json";
        }else
            url='/customers/?key='+key_v+'&value='+value_v+"&type=json&month="+month;
    }
    xhr.open('GET',url,false)
    xhr.send()
}
// find("dynamic");


fetch('/api/results_count', { method: "GET",mode: 'no-cors' })
    .then((res)=>(res.text()))
    .then((res)=>{
        // page_index=Number(res);
        let counts=Number(res);

        let pages=Math.ceil(counts/25);
        max_index=pages;
        // alert(pages);
        // console.log(res);
        // if ()
    })

// refresh_bar=()=>{
//     if(page_index==pages)

// }
