# -*- coding: utf-8 -*-

import json
import random
import string

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import FormView

from TOFI import models
from TOFI import send_mail as sm
from .forms import *


def main_view(request):
    if not request.user.is_anonymous:
        user = models.MyUser.objects.get(id=request.user.id)
        user.wrong_password_number = 0
        user.save()

        if request.user.is_admin:
            return HttpResponseRedirect("/mainadmin")
        if request.user.is_moder:
            return HttpResponseRedirect("/main_moder")
    rent = models.Rent.objects.all()
    l_rent = [{'address': i.address,
               'cost': i.cost, 'date_of_construction': i.date_of_construction,
               'name': i.name, 'area': i.area, 'min_rent_time': i.min_rent_time,
               'image_pic': i.images.first(), 'id': i.id} for i in list(rent)]
    context = {'rent': l_rent,
               'comments': models.Comment.objects.all(),
               'date': datetime.now()}
    return render(request, 'Main.html', context)


class AddRent(View):
    form_class = RentForm
    template_name = 'AddRent.html'

    def get(self, request):
        if request.user.is_anonymous:
            return HttpResponseRedirect("/login")
        if not request.user.ie:
            return HttpResponseRedirect('/')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        error = ''
        form = self.form_class(request.POST)
        print(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            min_rent_time = form.cleaned_data['min_rent_time']
            area = form.cleaned_data['area']
            date_of_construction = form.cleaned_data['date_of_construction']
            creation_date = date.today()
            other = form.cleaned_data['other']
            cost = form.cleaned_data['cost']
            cur_user = request.user
            payment_interval = form.cleaned_data['payment_interval']

            models.Rent.objects.create(name=name, address=address, min_rent_time=min_rent_time, area=area,
                                       date_of_construction=date_of_construction, creation_date=creation_date,
                                       other=other, cost=cost, user_login=cur_user, payment_interval=payment_interval)
            return HttpResponseRedirect('/')

        else:
            err = form.errors.as_data()
            print(err)
            if 'name' in err:
                error = 'Недопустимые символы в поле Имя!'
            if 'address' in err:
                error = 'Недопустимые символы в поле Адрес!'
            if 'min_rent_time' in err:
                error = 'Время ареннды должно быть от 1 до 365 дней!'
            if 'area' in err:
                error = 'Размер площади должен быть от 3 до 1000 кв.м.!'
            if 'date_of_construction' in err:
                error = 'Год постройки должен быть от 1950 до 2016 года!'
            if 'cost' in err:
                error = 'Цена должна быть в диапозоне от 1 до 1млн!'
            if 'payment_interval' in err:
                error = 'Интервал оплаты должен быть от 1 до 365 дней!'
            if 'other' in err:
                error = 'Недопустимые символы в описании дома!'
        return render(request, self.template_name, {'form': form, 'error': error})


class Registration(View):
    form_class = UserForm
    template_name = 'Registration.html'

    def get(self, request):
        if not request.user.is_anonymous and not request.user.is_admin:
            return HttpResponseRedirect("/")
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        error = ''

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
                elif user and not request.user.is_admin:
                    login(request, user)
                    return HttpResponseRedirect('/')
                if hasattr(request.user, 'is_admin'):
                    if request.user.is_admin:
                        return render(request, 'Admin/Done.html', {'message': 'Новая учетная запись успешно создана'})
            else:
                error = 'Пароли не совпадают!'

        else:
            err = form.errors.as_data()
            print(err)
            if 'password' in err:
                error = 'Пароль должен содержать арабские цифры и латинские буквы, нижнего и верхнего регистра!'
            if 'phone' in err:
                error = 'Недопустимый номер телефона!(Пример: +375 12 345 67 89)'
            if 'username' in err:
                error = 'Пользователь с таким логином уже существует!'
            if 'name' in err:
                error = 'Недопустимые символы в поле Имя!(Допустимы только буквы русского алфавита)'
            if 'surname' in err:
                error = 'Недопустимые символы в поле Фамилия!(Допустимы только буквы русского алфавита)'
            if 'last_name' in err:
                error = 'Недопустимые символы в поле Отчество!(Допустимы только буквы русского алфавита)'
            if 'age' in err:
                error = 'Недопустимое значение в поле Возраст!(Возраст должен быть от 18 до 110)'
            if 'email' in err:
                if 'My user with this Электронная почта already exists.' in err['email'][0]:
                    error = 'Пользователь с таким почтовым адресом уже зарегистрирован!'
                else:
                    error = 'Недопустимые символы в поле Email!(Пример: abcd@efg.com)'
            if 'address' in err:
                error = 'Недопустимые символы в поле Адрес!(Допустимы только буквы русского алфавита ' \
                        'и знаки пунктуации)'
            if 'passport_id' in err:
                if 'My user with this Номер паспорта already exists.' in err['passport_id'][0]:
                    error = 'Пользователь с таким номером паспорта уже зарегистрирован!'
                else:
                    error = 'Недопустимые символы в поле Номер пасспорта!(Пример: AB1234567)'
            if 'taxpayer_account_number' in err:
                error = 'Недопустимое значение в поле УНН!(Значение должно быть от 1 до 100000)'
            if 'license_field' in err:
                error = 'Недопустимые символы в поле Лицензия!(Допустимы только буквы русского и английского алфавита)'
        return render(request, self.template_name, {'form': form, 'error': error})


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

    def form_invalid(self, form):
        error = ''
        login_user = form.cleaned_data['username']
        user = None
        try:
            user = models.MyUser.objects.get(username=login_user)
            if not user.is_active:
                return render(self.request, 'BlockedAcc.html', {'us': user.username, 'reason': user.reason_block})
        except:
            pass

        if not user is None:
            user.wrong_password_number += 1
            user.save()
            if user.wrong_password_number == 4:
                error += "У вас осталась последняя попытка ввода корректного пароля! "
            if user.wrong_password_number == 5:
                user.reason_block = "5 раз ввёл некорректный пароль."
                user.is_active = 0
                user.save()

        error += ' Введены некорректные Логин и/или Пароль. Оба поля чувствительны к верхнему регистру!'
        return render(self.request, 'login.html', {'form': form, 'error': error})


def logout_view(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")
    logout(request)
    return HttpResponseRedirect("/")


def aboutHouse(request, number):
    try:
        house = models.Rent.objects.get(id=int(number))
    except:
        return HttpResponseRedirect('/')
    images = house.images.all()

    d = list(models.Rent.objects.all())
    for i in d:
        if i.getId() == number:
            rent = i

    return render(request, "AboutHouse.html", {'rent': rent, 'images': images})


def make_rent(request, number):
    if request.user.is_anonymous or not request.user.is_active:
        return HttpResponseRedirect("/login")
    try:
        rent = models.Rent.objects.all().get(id=number)
    except:
        return HttpResponseRedirect('/')
    user = models.MyUser.objects.all().get(id=str(rent.user_login.id))

    class MakeMessage(forms.Form):
        text_message = 'Запрос на аренду вашего дома под номером ' + str(number) + " (" + str(
            rent.name) + ") от " + str(request.user.name) + " " + str(request.user.surname) + " " + \
                       str(request.user.last_name) + "."

        text_message = forms.CharField(widget=forms.Textarea(attrs={'readonly': 'readonly', 'rows': '2',
                                                                    'class': 'form-control padding'}),
                                       label="Содержание:", max_length=100, required=True, initial=text_message, )
        text_more = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control padding',
                                                                 'placeholder': 'Введите сопроводительное письмо...',
                                                                 'rows': '4'}),
                                    label="Дополнительно:", max_length=100, required=True)

    if request.method == 'POST':
        form = MakeMessage(request.POST)

        if form.is_valid():
            text_more = form.cleaned_data['text_more']

            text_message = 'Запрос на аренду вашего дома под номером ' + str(number) + " (" + str(
                rent.name) + ") от " + str(request.user.name) + " " + str(request.user.surname) + " " + \
                           str(request.user.last_name)

            models.MessageStatusRent.objects.create(id_user_from=request.user.id, id_user_to=user.id,
                                                    creation_date=date.today(),
                                                    text_message=text_message, text_more=text_more, login_user_from=request.user.username, id_rent=number)
            mes = "Сообщение отправлено пользователю " + user.username

            return render(request, 'MessageDoned.html', {'mes': mes})

    else:
        form = MakeMessage()
    return render(request, "MakeRent.html", {'form': form, 'id': number})


def aboutUser(request, login_id):
    try:
        int(login_id)
        models.MyUser.objects.get(id=login_id)
    except:
        return HttpResponseRedirect('/')

    if request.method == 'GET':
        userList = list(models.MyUser.objects.all())
        for user in userList:
            if user.getId() == login_id:
                context = {'user': user}

        comments = models.CommentUser.objects.all().filter(id_user_about=login_id)

        class CommentUserTemp(object):
            def __init__(self, login_user_from, text_com, date_com):
                self.login_user_from = login_user_from
                self.text_com = text_com
                self.date = date_com

        user_comments = []
        for com in comments:
            us = models.MyUser.objects.get(id=com.id_user_from)
            user_comments.append(CommentUserTemp(us.username, com.text_comment, com.date_comment))
        context.update({'com': list(reversed(user_comments))})
        return render(request, "AboutUser.html", context)
    else:
        if request.user.is_anonymous or not request.user.is_active:
            return HttpResponseRedirect("/login")

        com = request.POST['comment']
        models.CommentUser.objects.create(id_user_about=login_id, id_user_from=request.user.id,
                                          text_comment=com, date_comment=date.today())
        response = {'com': com, 'user': request.user.username, 'date': date.today().strftime('%b. %d, %Y')}
        response = json.dumps(response, ensure_ascii=False)
        return HttpResponse(response, content_type="text/html; charset=utf-8")


def comment(request):
    if request.user.is_anonymous or not request.user.is_active:
        return HttpResponseRedirect("/login")

    if request.method == 'GET':
        context = {'com': list(reversed([i for i in list(models.Comment.objects.all())]))}
        return render(request, "Comment.html", context)
    else:
        com = request.POST['comment']
        models.Comment.objects.create(text_comment=com, user_login=request.user.username,
                                      date_comment=date.today())

        response = {'com': com, 'user': request.user.username, 'date': date.today().strftime('%b. %d, %Y')}
        response = json.dumps(response, ensure_ascii=False)
        return HttpResponse(response, content_type="text/html; charset=utf-8")


def make_complaint(request, id_user_to):
    if request.user.is_anonymous or not request.user.is_active:
        return HttpResponseRedirect("/login")

    if id_user_to == '0':
        class MakeComplaint(forms.Form):
            describe = forms.CharField(label="Опишите проблему:", max_length=150, required=True,
                                       widget=forms.Textarea(attrs={'rows': '4'}))

        if request.method == 'POST':
            form = MakeComplaint(request.POST)

            if form.is_valid():
                if request.user.is_anonymous:
                    login_user_from = "Guest"
                else:
                    login_user_from = request.user.username
                login_user_to = "message for moder"
                describe = form.cleaned_data['describe']
                models.Complaint.objects.create(login_user_from=login_user_from, login_user_to=login_user_to,
                                                describe=describe, date=date.today())
                mes = "Ваше письмо отправлено на сервер и будет рассмотрено в ближайшее время."

                return render(request, 'Profile/Thanks.html', {'mes': mes})

        else:
            form = MakeComplaint()
        return render(request, 'MakeComplaint.html', {'form': form})

    else:
        if request.user.is_anonymous:
            return HttpResponseRedirect("/login")
        user_to = models.MyUser.objects.get(id=id_user_to)

        class MakeComplaint(forms.Form):
            login_user_to = forms.CharField(label="Жалоба на :", max_length=100, required=True,
                                            widget=forms.TextInput(attrs={'readonly': 'readonly'}),
                                            initial=user_to.username)
            describe = forms.CharField(label="Опишите жалобу:", max_length=150, required=True,
                                       widget=forms.Textarea(attrs={'rows': '4'}))

        if request.method == 'POST':
            form = MakeComplaint(request.POST)

            if form.is_valid():
                login_user_from = request.user.username
                login_user_to = user_to.username
                describe = form.cleaned_data['describe']
                models.Complaint.objects.create(login_user_from=login_user_from, login_user_to=login_user_to,
                                                describe=describe, date=date.today())
                mes = "Ваша жалоба на пользователя " + user_to.username + " отправлена на сервер и " \
                                                                          "будет рассмотрена в ближайшее время."

                return render(request, 'Profile/Thanks.html', {'mes': mes})

        else:
            form = MakeComplaint()
        return render(request, 'MakeComplaint.html', {'form': form})


def reset_password(request):
    class ResetPassword(forms.Form):
        login = forms.CharField(label='Введите логин:', max_length=50, required=True)
        email = forms.CharField(label='Введите почтовый адрес:', max_length=50, required=True)

    error, no_error, result = '', '', False
    if request.method == 'POST':
        form = ResetPassword(request.POST)

        if form.is_valid():
            login = form.cleaned_data['login']
            email = form.cleaned_data['email']
            users = models.MyUser.objects.all()
            for us in users:
                if us.username == login:
                    if us.email == email:
                        new_password = "".join(
                            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in
                            range(16))

                        u = models.MyUser.objects.get(username=login)
                        u.set_password(new_password)
                        u.save()
                        sm.Sender("Смена пароля", "Смена пароля для аккаунта " + login +
                                  ". Вы подали запрос на смену пароля от вашего аккаунта. Ваш новый пароль: " +
                                  str(new_password), email).sender()

                        result = True
                        break
                    else:
                        result = False
                        break
            if not result:
                error = "Введены некорректные данные!"
            else:
                no_error = 'Новый пароль отослан на ваш почтовый ящик.'
    else:
        form = ResetPassword()
    form = ResetPassword()
    return render(request, 'ForgottenPassword.html', {'form': form, 'error': error, 'no_error': no_error})


def upload_pic(request, id_house):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            models.Rent.objects.get(id=id_house).images.add(
            models.ImageModel.objects.create(model_pic=form.cleaned_data['image'],
                                             name=form.cleaned_data['name'],
                                             describe=form.cleaned_data['describe']))
            return render(request, 'Profile/Thanks.html', {'mes': "Фотография успешно загружена на сервер."})
    else:
        form = ImageUploadForm()
    return render(request, 'add_image.html', {'form': form, 'id_house': id_house})
