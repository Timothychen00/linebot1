var page_index = 1;
var max_index = 10;
var search_mode = "total";
//search
//total
//this_month
//next_month

//find_mode可以通過var也可以通過傳遞變數

function change_mode(mode) {
    window.page_index = 1;
    document.getElementById('page_index').innerText = page_index;
    window.search_mode = mode;
    find();
}
// alert(3);

var next_page = () => {
    window.page_index += 1;
    find();//使用當前的var
    document.getElementById('page_index').innerText = page_index;
}

var last_page = () => {
    if (page_index > 1)
        window.page_index -= 1;
    find();
    document.getElementById('page_index').innerText = page_index;

}

function find(key_v = null, value_v = null) {
    // alert(search_mode);
    console.log(search_mode);
    //    alert(2);
    var start = (page_index - 1) * 25;
    if (search_mode == 'total') {
        // key_v=null;
        // value_v=null;
    } else if (search_mode == 'this_month' || search_mode == 'next_month') {
        key_v = 'next-time';
        value_v = '1';
    }else if(search_mode=='search')
    {
        key_v = document.getElementById('type').value;
        value_v = document.getElementById('value').value;
    }

    console.log(value);
    xhr = new XMLHttpRequest();

    // alert(page_index);
    // alert(start);
    // var start=1;
    table = document.querySelector("#place");
    xhr.onload = function (e) {
        // alert(1);
        var place = document.getElementById('place');
        //place.innerHTML=a[0]
        a = JSON.parse(xhr.response);
        console.log(a);
        var month = a[0];

        a.shift();
        console.log(a[1]);
        length = 25;
        place.innerHTML = "";
        for (let i = start; i < start+length; i++) {
            // place.innerHTML="";
            place.innerHTML += "\
            <tr>\
                <td>"+ a[i][0] + "</td>\
                <td><a href=\'/customers/"+ a[i][0] + "/\'>" + a[i][1] + "</a></td>\
                <td>"+ a[i][2] + "</td>\
                <td>"+ a[i][3] + "</td>\
                <td>\
                    <button type=\"button\" class=\"btn btn-danger\" data-bs-toggle=\"modal\" data-bs-target=\"#exampleModal"+ a[i][0] + "\">刪除</button>\
                    <div class=\"modal fade\" id=\"exampleModal"+ a[i][0] + "\" tabindex=\"-1\" aria-labelledby=\"exampleModalLabel\" aria-hidden=\"true\">\
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
                                    <button type=\"button\" class=\"btn btn-danger\" onclick=\"location.href=\'/customers/"+ a[i][0] + "/delete/ \'\" >確認刪除</button>\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                </td>\
            </tr>"
        }
    }
    // alert(month);
    var place = document.getElementById('place');
    url = '';
        place.innerHTML = '';
        if ( search_mode=='total'){
            url = '/customers/?type=json';
        }else if (search_mode == 'search') {
            url = '/customers/?key=' + key_v + '&value=' + value_v + "&type=json";
        } else if (search_mode == 'this_month' || search_mode == 'next_month'){
            url = '/customers/?key=' + key_v + '&value=' + value_v + "&type=json&month=" + search_mode;
        }
    // }
    xhr.open('GET', url, false)
    xhr.send()
}