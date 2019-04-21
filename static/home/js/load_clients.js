var xmlhttp = null;
if (window.XMLHttpRequest) {
    xmlhttp = new XMLHttpRequest();
} else if (window.ActiveXObject) {
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
}

if (xmlhttp != null) {
    xmlhttp.onreadystatechange=function(){
		if (this.readyState==4 && this.status==200){
			showClients(this);
		}
	}
    xmlhttp.open("GET", '/clients', true);
    xmlhttp.send(null);
} else {
    alert("浏览器不支持异步加载。");
}

function showClients(jData) {
    var d = JSON.parse(jData.responseText);
    var li = "";
    if (d) {
        for (i = 0; i <d.length; i++) {
            if (d[i].logo) {
                li += "<li><a href=" + d[i].home_url + "><img class='icon-img' src='/get-img?img_src=" + d[i].logo + "' alt=''/><span class='icon-desk'><span class='d-title'>" + d[i].company_name + "</span></span></a></li>";
            } else{
                li += "<li><a href=" + d[i].home_url + "><img class='icon-img' src='/static/home/img/mega_icon3.png' alt=''/><span class='icon-desk'><span class='d-title'>" + d[i].company_name + "</span></span></a></li>";
            }
        }
        document.getElementById("clients").innerHTML += li;
    }
}


