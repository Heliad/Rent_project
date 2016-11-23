from django.shortcuts import render, redirect
from TOFI import models
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.views.generic import View
from django.contrib.auth import logout
from .forms import UserForm, RentForm, RefillBalance, ChangePassword, DeleteMySelf
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


def refillBalance(request):
    if request.method == 'POST':
        form = RefillBalance(request.POST)

        if form.is_valid():
            card_num = form.cleaned_data['card_num']
            period_validity = form.cleaned_data['period_validity']
            name_card_owner = form.cleaned_data['name_card_owner']
            CVC2_CVV = form.cleaned_data['CVC2_CVV']
            size = form.cleaned_data['size']

            balance = request.user.balance
            newBalance = balance + size
            models.MyUser.objects.all().filter(username=request.user).update(balance=newBalance)
            context = {'mes': request.user.name + ", баланс успешно пополнен на " + str(size) + " BYN"}

            return render(request, 'Thanks.html', context)
    else:
        form = RefillBalance()

    return render(request, 'RefillBalance.html', {'form': form})


def unfillBalance(request):
    if request.method == 'POST':
        form = RefillBalance(request.POST)

        if form.is_valid():
            card_num = form.cleaned_data['card_num']
            period_validity = form.cleaned_data['period_validity']
            name_card_owner = form.cleaned_data['name_card_owner']
            CVC2_CVV = form.cleaned_data['CVC2_CVV']
            size = form.cleaned_data['size']

            balance = request.user.balance
            if balance >= size:
                newBalance = balance - size
                models.MyUser.objects.all().filter(username=request.user).update(balance=newBalance)
                context = {'mes': request.user.name + ", Срдества в размере: " + str(size) + " BYN были успешно выведены"}
            else:
                context = {'mes': "На вашем счете не хватает средств"}

            return render(request, 'Thanks.html', context)
    else:
        form = RefillBalance()

    return render(request, 'UnfillBalance.html', {'form': form})


def profileChangePassword(request):
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
                    return render(request, 'ChangePasswordDone.html')
                else:
                    error = 'Вы ввели неверный пароль'
            else:
                error = 'Пароли не совпадают'
    else:
        form = ChangePassword()

    return render(request, "ChangePassword.html", {'form': form, 'error': error})


def deleteMySelf(request):
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

    return render(request, "DeleteMySelf.html", {'form': form, 'error': error})

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