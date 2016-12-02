# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from TOFI import models
import json
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.views.generic import View
from django.contrib.auth import logout
from .forms import *
from TOFI import transaction as t
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
import datetime


def main_view(request):
    context = {'rent': [i for i in list(models.Rent.objects.all())], 'comments': [i for i in list(models.Comment.objects.all())]}
    return render(request, 'Main.html', context)


class AddRent(View):
    form_class = RentForm
    template_name = 'AddRent.html'

    def get(self, request):
        if request.user.is_anonymous:
            return HttpResponseRedirect("/login")
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        print(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            min_rent_time = form.cleaned_data['min_rent_time']
            area = form.cleaned_data['area']
            date_of_construction = form.cleaned_data['date_of_construction']
            creation_date = datetime.date.today()
            other = form.cleaned_data['other']
            cost = form.cleaned_data['cost']
            cur_user = request.user

            models.Rent.objects.create(name=name, address=address, min_rent_time=min_rent_time, area=area,
                                       date_of_construction=date_of_construction, creation_date=creation_date,
                                       other=other, cost=cost, user_login=cur_user.id)

            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})


class Registration(View):
    form_class = UserForm
    template_name = 'Registration.html'

    def get(self, request):
        if not request.user.is_anonymous:
            return HttpResponseRedirect("/")
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            if form.cleaned_data['password'] == form.cleaned_data['password1']:
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()

                user = authenticate(username=username, password=password)

                if user:
                    login(request, user)
                    return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form})


class Login(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return HttpResponseRedirect("/")
        return render(request, self.template_name,  {'form': self.form_class})

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(Login, self).form_valid(form)


def logout_view(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")
    logout(request)
    return HttpResponseRedirect("/")


def profile(request):
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
    return render(request, "Profile.html", {'cards':  cards, 'new': new, 'number': number})


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
                                                           describe_operation="Баланс успешно пополнен на " + str(size) + " BYN",
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
                                                               size) + " BYN",
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


def aboutHouse(request, number):
    d = list(models.Rent.objects.all())
    for i in d:
        if i.getId() == number:
            context = {'rent': i}

    return render(request, "AboutHouse.html", context)


def make_rent(request, number):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")
    rent = models.Rent.objects.all().get(id=number)
    user = models.MyUser.objects.all().get(id=str(rent.user_login))

    class MakeMessage(forms.Form):
        text_message = 'Запрос на аренду вашего дома под номером ' + str(number) + " (" + str(
            rent.name) + ") от " + str(request.user.name) + " " + str(request.user.surname) + " " + \
                       str(request.user.last_name)

        text_message = forms.CharField(label="Содержание:", initial=text_message)
        text_more = forms.CharField(label="Дополнительно:", max_length=100)

    if request.method == 'POST':
        form = MakeMessage(request.POST)

        if form.is_valid():
            text_more = form.cleaned_data['text_more']

            text_message = 'Запрос на аренду вашего дома под номером ' + str(number) + " (" + str(
                rent.name) + ") от " + str(request.user.name) + " " + str(request.user.surname) + " " + \
                           str(request.user.last_name)

            models.MessageStatusRent.objects.create(id_user_from=request.user.id, id_user_to=user.id,
                                                    creation_date=datetime.date.today(),
                                                    text_message=text_message, text_more=text_more, login_user_from=request.user.username, id_rent=number)
            mes = "Сообщение отправлено пользователю " + user.username

            return render(request, 'MessageDoned.html', {'mes': mes})

    else:
        form = MakeMessage()
    return render(request, "MakeRent.html", {'form': form})


def aboutUser(request, login_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")
    userList = list(models.MyUser.objects.all())
    for user in userList:
        if user.getId() == login_id:
            context = {'user': user}
    return render(request, "AboutUser.html", context)


def edit_profile(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")

    class EditProfile(forms.Form):
        email = forms.CharField(label="Почтовый адрес", max_length=50, required=True, initial=request.user.email)
        name = forms.CharField(label="Ваше имя", max_length=50, required=True, initial=request.user.name)
        surname = forms.CharField(label="Ваша фамилия", max_length=50, required=True, initial=request.user.surname)
        last_name = forms.CharField(label="Ваше отчество", max_length=50, required=True, initial=request.user.last_name)
        age = forms.IntegerField(label="Ваш возраст", required=True, initial=request.user.age)
        passport_id = forms.CharField(label="Номер вашего паспорта", max_length=50, required=True, initial=request.user.passport_id)
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
    accept = "Запрос номер " + str(message.id) + ", на аренду дома " + str(house.name)\
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

        c, m = t.Transaction(request.POST['size'], request.POST['card_from'], request.POST['balance_to']).make_transaction()
        response = {"message": m, "status": c}
        # Логирование операции оплаты аренды
        models.LogOperationsBalance.objects.create(id_user=request.user.id, type_operation='Оплата аренды',
                                                   describe_operation="Оплата на сумму " +
                                                                      str(request.POST['size']) + " BYN. " +
                                                   str(m), date_operation=datetime.date.today())

        response = json.dumps(response, ensure_ascii=False)
        return HttpResponse(response, content_type="text/html; charset=utf-8")


def add_comment(request):
    if request.method == 'POST':
        form = AddComment(request.POST)

        if form.is_valid():
            com = form.cleaned_data['text_comment']
            models.Comment.objects.create(text_comment=com, user_login=request.user.username, date_comment=datetime.date.today())

            return render(request, 'CommentDoned.html')
    else:
        form = AddComment()
        return render(request, "AddComment.html", {'form': form})


def all_comments(request):
    context = {'com': [i for i in list(models.Comment.objects.all())]}
    return render(request, "AllComments.html", context)


def search(request):
    return render(request, "Search/Search.html")


def search_rent(request):
    if request.method == 'POST':
        form = SearchRent(request.POST)

        if form.is_valid():
            results = []
            type_search = form.cleaned_data['type_search']
            max_interval = form.cleaned_data['max_interval']
            min_interval = form.cleaned_data['min_interval']
            login_or_name_rent = form.cleaned_data['login_or_name_rent']
            square = form.cleaned_data['square']
            if type_search == '1':
                temp = list(models.Rent.objects.all())
                for rent in temp:
                    if int(rent.cost) <= max_interval:
                        if int(rent.cost) >= min_interval:
                            results.append(rent)
            if type_search == '2':
                results = list(models.Rent.objects.all().filter(name=login_or_name_rent))
            if type_search == '3':
                user_id_login = models.MyUser.objects.get(username=login_or_name_rent)
                results = list(models.Rent.objects.all().filter(user_login=user_id_login.id))
            if type_search == '4':
                temp = list(models.Rent.objects.all())
                for rent in temp:
                    if int(rent.area) <= square:
                        results.append(rent)

            return render(request, 'Search/SearchRent.html', {'form': form, 'results': results})
    else:
        form = SearchRent()
        return render(request, "Search/SearchRent.html", {'form': form})


def search_user(request):
    if request.method == 'POST':
        form = SearchUser(request.POST)

        if form.is_valid():
            results = None
            type_search = form.cleaned_data['type_search']
            attr_search = form.cleaned_data['field_search']
            if type_search == '1':
                results = models.MyUser.objects.all().filter(username=attr_search)
            if type_search == '2':
                results = models.MyUser.objects.all().filter(surname=attr_search)
            if type_search == '3':
                results = models.MyUser.objects.all().filter(email=attr_search)
            return render(request, 'Search/SearchUser.html', {'form': form, 'results': results})
    else:
        form = SearchUser()
        return render(request, "Search/SearchUser.html", {'form': form})