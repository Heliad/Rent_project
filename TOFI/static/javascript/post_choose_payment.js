function pay_rent(card_id) {
    var amount = document.getElementById('amount');
    if (check_data(amount) == 0) {
        return 0
    }
    amount = amount.value;
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
                var div = document.getElementById('response');
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

function fill_balance(card_id, type) {
    var amount = document.getElementById('amount');
    if (check_data(amount) == 0) {
        return 0
    }
    amount = Number(amount.value);
    var xmlhttp = getXmlHttp();
    var params = 'card_from=' + encodeURIComponent(card_id) +
        '&size=' + encodeURIComponent(amount) + '&type=' + encodeURIComponent(type);
    params += '&csrfmiddlewaretoken=' + document.getElementsByName('csrfmiddlewaretoken')[0].value;
    xmlhttp.open("POST", 'refillbalance/', true);
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send(params);
    var b = document.getElementsByTagName('input');
    for (var i = 0; i < b.length; i++) {
        b[i].disabled = true;
    }
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4) {
            var div = document.getElementById('response');
            if (JSON.parse(xmlhttp.responseText)["status"] == true) {
                div.style.color = "green";
                div.innerHTML = JSON.parse(xmlhttp.responseText)["message"];
                window.setTimeout(function () {
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
    if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
        xmlhttp = new XMLHttpRequest();
    }
    return xmlhttp;
}


function amount_onfocus() {
    var amount = document.getElementById('amount');
    amount.placeholder = "Сумма";
    amount.style.borderColor = "lightgray";
    amount.className = "form-control height70 formValid";
}

function amount_oninput() {
    document.getElementById('response').innerHTML = "";
    var amount = document.getElementById('amount');
    var mon_notification = document.getElementById('mon_notification');
    if (amount.value.slice(amount.value.indexOf('.')).length > 3) {
        amount.value = amount.value.slice(0, -1);
    }
    if (Number(amount.value) > 0 && Number(amount.value)) {
        if (Number(amount.value).toFixed(2) != Number(amount.value)) {
            amount.value = Number(amount.value.slice(0, -1)).toFixed(2)
        }
        var num = (Number(amount.value) * Number(document.getElementById('mon_value').innerHTML) + Number(amount.value)).toFixed(2);
        if (num == "Infinity" || Number(amount.value) > 10000) {
            mon_notification.innerHTML = 'Сумма без комиссии до 10000 BYN'
        }
        else {
            mon_notification.innerHTML = 'Игото к оплате (+ коммисия ' + Number(document.getElementById('mon_value').innerHTML) * 100 + '%): ' + num + ' BYN'
        }
    }
    else {
        mon_notification.innerHTML = ''
    }
}

function add_card() {
    var card_num = document.getElementById('id_card_num').value;
    var period_validity = document.getElementById('id_period_validity').value;
    var name_card_owner = document.getElementById('id_name_card_owner').value;
    var CVC2_CVV = document.getElementById('id_CVC2_CVV').value;
    var xmlhttp = getXmlHttp();
    var params = 'card_num=' + encodeURIComponent(card_num) +
        '&period_validity=' + encodeURIComponent(period_validity) +
        '&name_card_owner=' + encodeURIComponent(name_card_owner) +
        '&CVC2_CVV=' + encodeURIComponent(CVC2_CVV);
    params += '&csrfmiddlewaretoken=' + document.getElementsByName('csrfmiddlewaretoken')[0].value;
    xmlhttp.open("POST", 'add_card/', true);
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xmlhttp.send(params);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4) {
            document.getElementById('card_num').innerHTML = '';
            document.getElementById('period_validity').innerHTML = '';
            document.getElementById('name_card_owner').innerHTML = '';
            document.getElementById('CVC2_CVV').innerHTML = '';
            var div = document.getElementById('response');
            if (JSON.parse(xmlhttp.responseText)["status"] == true) {
                div.style.color = "green";
                div.innerHTML = JSON.parse(xmlhttp.responseText)["mes"];
                var b = document.getElementsByTagName('Button');
                b[0].disabled = true;
                window.setTimeout(function () {
                    var new_url = "/profile";
                    window.location.replace(new_url)
                }, 2000);
            }
            else {
                div.style.color = "red";
                if (JSON.parse(xmlhttp.responseText)["errors"] != null) {
                    var error = JSON.parse(xmlhttp.responseText)["errors"];
                    for (var i = 0; i < error.length; i++) {
                        for (var j in error[i]) {
                            document.getElementById(j).innerHTML += error[i][j];
                        }
                    }
                }
                else if (JSON.parse(xmlhttp.responseText)["mes"] != null) {
                    div.style.color = "red";
                    div.innerHTML = JSON.parse(xmlhttp.responseText)["mes"];
                }
            }
        }
    }
}


function check_data(a) {
    amount = a;
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
    else if (Number(amount.value) > 10000) {
        amount.value = "";
        amount.className = "form-control height70 formInvalid";
        amount.placeholder = "Сумма до 10000 BYN";
        amount.style.borderColor = "red";
        return 0;
    }
    return 1;
}
