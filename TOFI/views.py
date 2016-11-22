from django.shortcuts import render, redirect
from TOFI import models
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from django.contrib.auth import logout
from .forms import UserForm, RentForm
from django.http import HttpResponseRedirect
import datetime


def main_view(request):
    context = {'rent': [i for i in list(models.Rent.objects.all())]}
    return render(request, 'Main.html', context)


class AddRent(View):
    form_class = RentForm
    template_name = 'AddRent.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
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

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(Login, self).form_valid(form)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def profile(request):
    return render(request, "Profile.html")


def profileChangePassword(request):
    return render(request, "ChangePassword.html")


def aboutHouse(request, number):
    d = list(models.Rent.objects.all())
    for i in d:
        if i.getId() == number:
            context = {'rent': i}

    return render(request, "AboutHouse.html", context)


def aboutUser(request, login_id):
    userList = list(models.MyUser.objects.all())
    for user in userList:
        if user.getId() == login_id:
            context = {'user': user}
    return render(request, "AboutUser.html", context)