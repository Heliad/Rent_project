    function func(card_id, balance_to, amount, id) {
        var xmlhttp = getXmlHttp();
        var params = 'card_from=' + encodeURIComponent(card_id) +
                '&size=' + encodeURIComponent(amount) + '&balance_to=' + encodeURIComponent(balance_to);
        if (document.getElementById('check_box').checked)
        {
            params += '&is_save=' + true;
        }
        else
        {
            params += '&is_save=' + false;
        }
        params += '&csrfmiddlewaretoken=' + document.getElementsByName('csrfmiddlewaretoken')[0].value;
        xmlhttp.open("POST", id, true);
        xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xmlhttp.send(params);
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4){
                div = document.getElementById('response');
                if (JSON.parse(xmlhttp.responseText)["status"] == true){
                    div.style.color = "green";
                    div.innerHTML = JSON.parse(xmlhttp.responseText)["message"];
                    window.setTimeout(function() {
                        var new_url = "/profile";
                        window.location.replace(new_url)
                    }, 2000);
                }
                else {
                    div.style.color = "red";
                    div.innerHTML = JSON.parse(xmlhttp.responseText)["message"];
                }
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

