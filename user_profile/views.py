import datetime
import json

from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from TOFI import models
from TOFI import transaction as t
from TOFI import check as ch
from TOFI.forms import *


def profile(request):
    ch.check_rent_number_pay()

    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")
    cards = list()
    for card in [str(i.card_num) for i in request.user.user_card_id.all()]:
        cards.append(card[:4] + ' XXXX XXXX ' + card[-4:])

    mails = models.MessageStatusRent.objects.all().filter(id_user_to=request.user.id)
    new, number = False, 0

    for mail in mails:
        if mail.is_new:
            new = True
            number += 1

    penalties = models.DonePenalty.objects.filter(id_user_for=request.user.id)
    return render(request, "Profile.html", {'cards': cards, 'new': new, 'number': number, 'penalties': penalties})


def add_card(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")

    class AddCard(forms.Form):
        card_num = forms.CharField(label="Номер карты/Card number", max_length=16, required=True)
        period_validity = forms.CharField(label="Срок действия (ММГГ)", max_length=5, required=True)
        name_card_owner = forms.CharField(label="Имя держателя карты", max_length=50, required=True)
        CVC2_CVV = forms.CharField(label="CVC2/CVV", max_length=3, required=True)

    if request.method == 'POST':
        form = AddCard(request.POST)

        if form.is_valid():
            card_num = form.cleaned_data['card_num']
            period_validity = form.cleaned_data['period_validity']
            name_card_owner = form.cleaned_data['name_card_owner']
            CVC2_CVV = form.cleaned_data['CVC2_CVV']
            if t.Check(card_num, period_validity, name_card_owner, CVC2_CVV).check_card():
                for i in request.user.user_card_id.all():
                    if i.card_num == card_num:
                        return render(request, 'Profile/Thanks.html', {'mes': 'карта уже добавлена'})
                request.user.user_card_id.add(models.UserCard.objects.get(card_num=card_num))
                return render(request, 'Profile/Thanks.html', {'mes': 'карта успешно добавлена'})
            else:
                return render(request, 'Profile/Thanks.html', {'mes': 'Неверные данные', 'redirect_address': 'profile'})
    else:
        form = AddCard()

    return render(request, 'Profile/RefillBalance.html', {'form': form})


def refillBalance(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")
    if request.method == 'POST':
        form = RefillBalance(request.POST)

        if form.is_valid():
            card_num = form.cleaned_data['card_num']
            period_validity = form.cleaned_data['period_validity']
            name_card_owner = form.cleaned_data['name_card_owner']
            CVC2_CVV = form.cleaned_data['CVC2_CVV']
            size = form.cleaned_data['size']

            if t.Check(card_num, period_validity, name_card_owner, CVC2_CVV).check_card():
                t.Transaction(size, card_num, request.user).make_transaction()

                # Логирование операции пополнения баланса
                models.LogOperationsBalance.objects.create(id_user=request.user.id, type_operation='Пополнение баланса',
                                                           describe_operation="Баланс успешно пополнен на " + str(
                                                               size) + " BYN",
                                                           date_operation=datetime.date.today())

                context = {'mes': request.user.name + ", баланс успешно пополнен на " + str(size) + " BYN"}
                return render(request, 'Profile/Thanks.html', context)
            else:
                return render(request, 'Profile/Thanks.html', {'mes': 'message'})
    else:
        form = RefillBalance()

    return render(request, 'Profile/RefillBalance.html', {'form': form})


def unfillBalance(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")
    if request.method == 'POST':
        form = RefillBalance(request.POST)

        if form.is_valid():
            card_num = form.cleaned_data['card_num']
            period_validity = form.cleaned_data['period_validity']
            name_card_owner = form.cleaned_data['name_card_owner']
            CVC2_CVV = form.cleaned_data['CVC2_CVV']
            size = form.cleaned_data['size']

            context = {'mes': ''}
            if t.Check(card_num, period_validity, name_card_owner, CVC2_CVV).check_card():
                t.Transaction(size, request.user, card_num).make_transaction()

                # Логирование операции вывода средств
                models.LogOperationsBalance.objects.create(id_user=request.user.id, type_operation='Вывод средств',
                                                           describe_operation="Вывод средств на сумму " + str(
                                                               size) + " BYN, успешно проведён.",
                                                           date_operation=datetime.date.today())

                context = {'mes': request.user.name + ", средства на сумму " + str(size) +
                                  " BYN, успешно выведены на карту"}

            return render(request, 'Profile/Thanks.html', context)
    else:
        form = RefillBalance()

    return render(request, 'Profile/UnfillBalance.html', {'form': form})


def profileChangePassword(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")
    error = ''
    if request.method == 'POST':
        form = ChangePassword(request.POST)

        if form.is_valid():
            oldPassword = form.cleaned_data['old_password']
            newPassword = form.cleaned_data['new_password']
            newPasswordRepeat = form.cleaned_data['new_password_repeat']

            currentPassword = request.user.password
            if newPassword == newPasswordRepeat:
                if check_password(oldPassword, currentPassword):

                    user = request.user
                    user.set_password(newPassword)
                    user.save()
                    return render(request, 'Profile/ChangePasswordDone.html')
                else:
                    error = 'Вы ввели неверный пароль'
            else:
                error = 'Пароли не совпадают'
    else:
        form = ChangePassword()

    return render(request, "Profile/ChangePassword.html", {'form': form, 'error': error})


def deleteMySelf(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")
    error = ''
    if request.method == 'POST':
        form = DeleteMySelf(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']

            currentPassword = request.user.password
            if check_password(password, currentPassword):
                curUser = request.user
                logout(request)
                curUser.delete()
                return HttpResponseRedirect("/")
            else:
                error = 'Вы ввели неверный пароль'
    else:
        form = DeleteMySelf()

    return render(request, "Profile/DeleteMySelf.html", {'form': form, 'error': error})


def edit_profile(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")

    class EditProfile(forms.Form):
        email = forms.CharField(label="Почтовый адрес", max_length=50, required=True, initial=request.user.email)
        name = forms.CharField(label="Ваше имя", max_length=50, required=True, initial=request.user.name)
        surname = forms.CharField(label="Ваша фамилия", max_length=50, required=True, initial=request.user.surname)
        last_name = forms.CharField(label="Ваше отчество", max_length=50, required=True, initial=request.user.last_name)
        age = forms.IntegerField(label="Ваш возраст", required=True, initial=request.user.age)
        passport_id = forms.CharField(label="Номер вашего паспорта", max_length=50, required=True,
                                      initial=request.user.passport_id)
        phone = forms.CharField(label="Ваш номер телефона", max_length=50, required=True, initial=request.user.phone)
        address = forms.CharField(label="Ваш адрес", max_length=50, required=True, initial=request.user.address)

    if request.method == 'POST':
        form = EditProfile(request.POST)

        if form.is_valid():
            user = request.user
            user.email = form.cleaned_data['email']
            user.name = form.cleaned_data['name']
            user.surname = form.cleaned_data['surname']
            user.last_name = form.cleaned_data['last_name']
            user.age = form.cleaned_data['age']
            user.passport_id = form.cleaned_data['passport_id']
            user.phone = form.cleaned_data['phone']
            user.address = form.cleaned_data['address']
            user.save()
            return render(request, 'Profile/EditProfileDone.html')

    else:
        form = EditProfile()
    return render(request, "Profile/EditProfile.html", {'form': form})


def mails(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/")
    mails = models.MessageStatusRent.objects.all().filter(id_user_to=request.user.id)

    for mail in mails:
        mail.is_new = False
        mail.save()
    return render(request, "Profile/Mails.html", {'mails': mails})


def accept_rent(request, id_mes):
    message = models.MessageStatusRent.objects.get(id=id_mes)
    house = models.Rent.objects.get(id=message.id_rent)

    models.DoneRent.objects.create(id_house=message.id_rent, id_user_owner=message.id_user_to,
                                   id_user_renter=message.id_user_from, date_rent=datetime.date.today(),
                                   cost=house.cost, pay_number=0, paid_user=0)

    message.is_done = True
    house.status_rent = False
    house.save()
    message.save()

    user = models.MyUser.objects.get(id=message.id_user_from)
    accept = "Запрос номер " + str(message.id) + ", на аренду дома " + str(house.name) \
             + "подтверждён. Запрос от" + str(user.username)
    return render(request, "Profile/AcceptRent.html", {'mes': accept})


def reject_rent(request, id_mes):
    if request.method == 'POST':
        form = RejectRent(request.POST)

        if form.is_valid():
            reason = form.cleaned_data['reject_reason']
            message = models.MessageStatusRent.objects.get(id=id_mes)
            house = models.Rent.objects.get(id=message.id_rent)
            text_message = 'Отказ на запрос о аренде дома под номером: ' + str(house.id) + " (" + \
                           str(house.name) + ")"

            models.MessageStatusRent.objects.create(id_user_from=request.user.id, id_user_to=message.id_user_from,
                                                    creation_date=datetime.date.today(),
                                                    text_message=text_message, text_more=reason,
                                                    login_user_from=request.user.username, id_rent=message.id_rent)

            reject = "В запросе, номер " + str(message.id) + ", на аренду дома: " + str(house.name) \
                     + " отказано"
            return render(request, "Profile/AcceptRent.html", {'mes': reject})
    else:
        form = RejectRent()
        return render(request, "Profile/RejectRent.html", {'form': form})


def all_rents_renter(request):
    id_user = request.user.id
    my_rents = models.DoneRent.objects.all().filter(id_user_renter=id_user)
    return render(request, 'Profile/AllRentsRentor.html', {'my_rents': my_rents})


def all_rents_owner(request):
    id_user = request.user.id
    my_rents = models.DoneRent.objects.all().filter(id_user_owner=id_user)
    return render(request, 'Profile/AllRentsOwner.html', {'my_rents': my_rents})


def choose_payment(request, id_donerent):
    if request.method == "GET":
        user_cards = request.user.user_card_id.all()
        cards_num = list(map(lambda x: x[:4] + ' XXXX XXXX ' + x[-4:],
                             [str(i.card_num) for i in request.user.user_card_id.all()]))
        cost = models.DoneRent.objects.get(id=id_donerent)
        balance_to = models.MyUser.objects.get(id=cost.id_user_owner).username
        return render(request, "Profile/ChoosePayment.html", {'amount': cost.cost, 'cards': zip(user_cards, cards_num),
                                                              'id': id_donerent, 'balance_to': balance_to})
    else:

        c, m = t.Transaction(request.POST['size'], request.POST['card_from'],
                             request.POST['balance_to'], True).make_transaction()

        if c:
            drent = models.DoneRent.objects.get(id=id_donerent)
            drent.paid_user += 1
            drent.save()

        response = {"message": m, "status": c}

        # Логирование операции оплаты аренды
        if c:
            models.LogOperationsBalance.objects.create(id_user=request.user.id, type_operation='Оплата аренды',
                                                       describe_operation="Оплата на сумму " +
                                                                          str(request.POST['size']) + " BYN. " +
                                                                          str(m), date_operation=datetime.date.today())

        response = json.dumps(response, ensure_ascii=False)

        if request.POST['card_from'] == request.user.username:
            card_from = 'Кошелек'
        else:
            card_from = request.POST['card_from']
        if request.POST['is_save'] == 'true' and not models.QuickPayment.objects.filter(username=request.user,
                                                                                        rent=models.DoneRent.objects.get(
                                                                                            id=id_donerent),
                                                                                        user_payment=card_from,
                                                                                        amount=request.POST['size']):
            models.QuickPayment.objects.create(username=request.user,
                                               rent=models.DoneRent.objects.get(id=id_donerent),
                                               user_payment=card_from,
                                               amount=request.POST['size'])
        return HttpResponse(response, content_type="text/html; charset=utf-8")


def extract_balance(request):
    if request.method == 'POST':
        form = ExtractBalance(request.POST)

        if form.is_valid():
            period_start = form.cleaned_data['period_start']
            period_end = form.cleaned_data['period_end']
            extracts = models.LogOperationsBalance.objects.filter(id_user=request.user.id)
            result = []
            for ex in extracts:
                if period_end >= ex.date_operation >= period_start:
                    result.append(ex)

            return render(request, 'Profile/ExtractBalance.html', {'form': form, 'result': result})
    else:
        form = ExtractBalance()
        return render(request, "Profile/ExtractBalance.html", {'form': form})


def quick_payment(request):
    if request.method == 'GET':
        list_payments = list()
        payments = models.QuickPayment.objects.filter(username=request.user)
        for i in payments:
            list_payments.append([i, i.user_payment, i.amount,
                                  models.Rent.objects.get(id=models.DoneRent.objects.get(id=i.rent_id).id_house).name])
        return render(request, 'Profile/QuickPayment.html', {'payments': list_payments})


def quick_payment_info(request, id):
    if request.method == 'GET':
        payment = models.QuickPayment.objects.get(id=id)
        return render(request, 'Profile/QuickPaymentInfo.html', {'payment': payment,
                                                                 'rent': models.Rent.objects.get(
                                                                     id=models.DoneRent.objects.get(
                                                                         id=payment.rent_id).id_house)})
    else:
        payment = models.QuickPayment.objects.get(id=id)
        if payment.user_payment == 'Кошелек':
            tr_from = request.user
        else:
            tr_from = models.UserCard.objects.get(card_num=payment.user_payment)
        tr_to = models.MyUser.objects.get(
            id=models.Rent.objects.get(id=models.DoneRent.objects.get(id=payment.rent_id).id_house).user_login)
        c, m = t.Transaction(payment.amount, tr_from, tr_to).make_transaction()
        return render(request, 'Profile/Thanks.html', {'mes': m})


def my_penalties(request):
    my_pen = models.DonePenalty.objects.filter(id_user_for=request.user.id)
    return render(request, 'Profile/MyPenalties.html', {'pen': my_pen})


def make_pay_penalty(request, id_penalty):
    my_pens = models.DonePenalty.objects.filter(id=id_penalty)

    pen = my_pens.get(id=id_penalty)
    id_done_rent = pen.id_done_rent

    done_rent = models.DoneRent.objects.get(id=id_done_rent)

    if done_rent.paid_user < done_rent.pay_number:
            return render(request, 'Profile/MyPenalties.html',
                  {'pen': my_pens, 'message': "Сначала оплатите задолженность за аренду."})

    else:
        user_from = models.MyUser.objects.get(id=done_rent.id_user_renter)
        user_to = models.MyUser.objects.get(id=done_rent.id_user_owner)
        c, m = t.Transaction(pen.size_penalty, user_from,
                             user_to, True).make_transaction()

        if c:
            models.LogOperationsBalance.objects.create(id_user=request.user.id, type_operation='Оплата штрафа за просрочку аренды',
                                                       describe_operation="Оплата на сумму " +
                                                                          str(pen.size_penalty) + " BYN. " +
                                                                          str(m), date_operation=datetime.date.today())
            pen.is_payd = True
            pen.save()

        return render(request, 'Profile/MyPenalties.html',
                    {'pen': my_pens, 'message': "Штраф оплачен.", 'stat': m})


def my_all_houses_owner(request):
    id_user = request.user.id
    houses = models.Rent.objects.filter(user_login=id_user)
    return render(request, 'Profile/MyAllHousesOwner.html', {'houses': houses})


def edit_my_house(request, id_rent):
    rent = models.Rent.objects.get(id=id_rent)

    class EditRent(forms.Form):
        name = forms.CharField(label="Название:", max_length=50, required=True, initial=rent.name)
        address = forms.CharField(label="Адрес:", max_length=50, required=True, initial=rent.address)
        min_rent_time = forms.IntegerField(label="Срок аренды:", required=True, initial=rent.min_rent_time)
        area = forms.IntegerField(label='Площадь:', required=True, initial=rent.area)
        date_of_construction = forms.IntegerField(label='Год строительства:', required=True, initial=rent.date_of_construction)
        other = forms.CharField(label="Другое:", max_length=100, required=True, initial=rent.other,
                                widget=forms.Textarea(attrs={'placeholder': 'Введите описание дома...', 'rows': '4'}))
        cost = forms.CharField(label='Цена аренды:', max_length=50, required=True, initial=rent.cost)

    if request.method == 'POST':
        form = EditRent(request.POST)
        if form.is_valid():
            rent.name = form.cleaned_data['name']
            rent.address = form.cleaned_data['address']
            rent.min_rent_time = form.cleaned_data['min_rent_time']
            rent.area = form.cleaned_data['area']
            rent.date_of_construction = form.cleaned_data['date_of_construction']
            rent.other = form.cleaned_data['other']
            rent.cost = form.cleaned_data['cost']
            rent.save()
            message = 'Данные о доме под названием: ' + rent.name + ' успешно обновлены и сохранены!'
            return render(request, 'Profile/Thanks.html', {'mes': message})

    else:
        form = EditRent()
        return render(request, 'Profile/EditMyRent.html', {'form': form})


def delete_my_house(request, id_rent):
    rent = models.Rent.objects.get(id=id_rent)
    if rent.status_rent:
        message = 'Дом под названием ' + rent.name + ' успешно удален!'
        rent.delete()
    else:
        message = 'Дом под названием ' + rent.name + ' не может быть удален! Он арендован.'
    return render(request, 'Profile/Thanks.html', {'mes': message})


def auto_payment(request):
    auto_payments = models.AutoPayment.objects.filter(user_id=request.user)

    return render(request, 'Profile/AutoPayment/AutoPayment.html', {'auto_payment': auto_payment})