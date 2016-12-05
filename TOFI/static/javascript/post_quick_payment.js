    function func(id) {
        var xmlhttp = getXmlHttp();
        var params = 'id=' + encodeURIComponent(id);
        params += '&csrfmiddlewaretoken=' + document.getElementsByName('csrfmiddlewaretoken')[0].value;
        xmlhttp.open("POST", true);
        xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xmlhttp.send(params);
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4) {
                div = document.getElementById('response');
                div.innerHTML = xmlhttp.response
            }
        }
    }

    function getXmlHttp(){
        var xmlhttp;
        try {
            xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
            } catch (e) {
        try {
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (E) {
        xmlhttp = false;
        }
    }
    if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
        xmlhttp = new XMLHttpRequest();
    }
    return xmlhttp;
    }
