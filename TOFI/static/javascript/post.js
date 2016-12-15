function func() {
    var xmlhttp = getXmlHttp();
    var params = 'username=' + document.getElementById('id_username').value +
        '&password=' + document.getElementById('id_password').value;
    params += '&csrfmiddlewaretoken=' + document.getElementsByName('csrfmiddlewaretoken')[0].value;
    xmlhttp.open("POST", '', true);
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send(params);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4) {
            try {
                var response = JSON.parse(xmlhttp.responseText)["response"];
            } catch (e) {
                window.location.replace('/')
            }
        }
    }
}

function getXmlHttp() {
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
    if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {
        xmlhttp = new XMLHttpRequest();
    }
    return xmlhttp;
}
