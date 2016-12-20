function get(url) {
    var xmlhttp = getXmlHttp();
    xmlhttp.open("GET", url, false);
    xmlhttp.send(null);
    if (xmlhttp.status == 200) {
        return xmlhttp.responseText;
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
