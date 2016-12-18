function func(card_id) {
    amount = document.getElementById('amount');
    if (amount.value == "") {
        amount.className = "form-control height70 formInvalid";
        amount.placeholder = "Введите сумму оплаты";
        amount.style.borderColor = "red";
        return 0;
    }
    else if (Number(amount.value) < 0 || !(Number(amount.value)) || (Number(amount.value) == "Infinity")) {
        amount.value = "";
        amount.className = "form-control height70 formInvalid";
        amount.placeholder = "Введите корректные данные";
        amount.style.borderColor = "red";
        return 0;
    }
    var amount = amount.value;
    var balance_to = document.getElementById('user').innerHTML;
    var id = document.getElementById('rent').innerHTML;
    amount = Number(amount);
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
    xmlhttp.open("POST", 'choose_payment/' + id, true);
        xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xmlhttp.send(params);
    var b = document.getElementsByTagName('input');
    for (var i = 0; i < b.length; i++) {
        b[i].disabled = true;
    }
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
                    for (var i = 0; i < b.length; i++) {
                        b[i].disabled = false;
                    }
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

document.getElementById('amount').onfocus = function () {
    var amount = document.getElementById('amount');
    amount.placeholder = "Сумма";
    amount.style.borderColor = "lightgray";
    amount.className = "form-control height70 formValid";
};

document.getElementById('amount').oninput = function () {
    document.getElementById('response').innerHTML = "";
    var amount = document.getElementById('amount');
    var mon_notification = document.getElementById('mon_notification');
    if (Number(amount.value) > 0 && Number(amount.value)) {
        var num = (Number(amount.value) * Number(document.getElementById('mon_value').innerHTML) + Number(amount.value)).toFixed(2);
        if (num == "Infinity") {
            mon_notification.innerHTML = ''
        }
        else {
            mon_notification.innerHTML = 'Игото к оплате: ' + num + ' BYN'
        }
    }
    else {
        mon_notification.innerHTML = ''
    }
};
