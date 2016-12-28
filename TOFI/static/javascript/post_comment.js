function func() {
        var xmlhttp = getXmlHttp();
    var comment = document.getElementById('comment');
    if (comment.value && is_spaces(comment.value) == 0) {
        var params = 'comment=' + encodeURIComponent(comment.value);
        params += '&csrfmiddlewaretoken=' + document.getElementsByName('csrfmiddlewaretoken')[0].value;
        xmlhttp.open("POST", '', true);
        xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xmlhttp.send(params);
        comment.value = '';
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4) {
                var response = document.getElementById('response');
                response.innerHTML = '<tr class="padding">' +
                    '<td class="padding">' + JSON.parse(xmlhttp.responseText)["user"] + '</td>' +
                    '<td class="text-center text-muted">' + JSON.parse(xmlhttp.responseText)["date"] + '</td>' +
                    '<td>' + JSON.parse(xmlhttp.responseText)["com"] + '</td>' + '</tr>' + response.innerHTML;
            }
            }
        }
    else {
        comment.value = '';
    }
}

function is_spaces(val) {
    for (var i = 0; i < val.length; i++) {
        if (val[i] != ' ') {
            return 0;
        }
    }
    return 1;
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
