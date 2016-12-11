# -*- coding: utf-8 -*-

import datetime
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import FormView

from TOFI import models
from .forms import *


def main_view(request):
    if not request.user.is_anonymous:
        if request.user.is_admin:
            return HttpResponseRedirect("/mainadmin")
        if request.user.is_moder:
            return HttpResponseRedirect("/main_moder")
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
            if 'phone' in err:
                error = 'Недопустимый номер телефона!'
            if 'username' in err:
                error = 'Пользователь с таким логином уже существует!'
            if 'name' in err:
                error = 'Недопустимые символы в поле Имя!'
            if 'surname' in err:
                error = 'Недопустимые символы в поле Фамилия!'
            if 'last_name' in err:
                error = 'Недопустимые символы в поле Отчество!'
            if 'age' in err:
                error = 'Недопустимые значение в поле Возраст!'
            if 'email' in err:
                error = 'Недопустимые значение в поле Email!'
            if 'address' in err:
                error = 'Недопустимые значение в поле Адрес!'
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


def logout_view(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect("/login")
    logout(request)
    return HttpResponseRedirect("/")


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
                       str(request.user.last_name) + "."

        text_message = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly', 'rows': '2'}),
                                       label="Содержание:",max_length=100, required=True, initial=text_message)
        text_more = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Введите сопроводительное письмо...', 'rows': '4'}),
                                    label="Дополнительно:", max_length=100, required=True)

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
        com = request.POST['comment']
        models.CommentUser.objects.create(id_user_about=login_id, id_user_from=request.user.id,
                                          text_comment=com, date_comment=datetime.date.today())
        response = {'com': com, 'user': request.user.username, 'date': datetime.date.today().strftime('%b. %d, %Y')}
        response = json.dumps(response, ensure_ascii=False)
        return HttpResponse(response, content_type="text/html; charset=utf-8")


def comment(request):
    if request.method == 'GET':
        context = {'com': list(reversed([i for i in list(models.Comment.objects.all())]))}
        return render(request, "Comment.html", context)
    else:
        com = request.POST['comment']
        models.Comment.objects.create(text_comment=com, user_login=request.user.username,
                                      date_comment=datetime.date.today())
        response = {'com': com, 'user': request.user.username, 'date': datetime.date.today().strftime('%b. %d, %Y')}
        response = json.dumps(response, ensure_ascii=False)
        return HttpResponse(response, content_type="text/html; charset=utf-8")
