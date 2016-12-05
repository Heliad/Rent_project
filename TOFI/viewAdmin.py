from django.http import HttpResponseRedirect
from django.shortcuts import render
from TOFI import models
from .forms import *

def main_admin(request):
    return render(request, 'Admin/MainAdmin.html')


def blocked_accounts(request):
    blocked_accounts = models.MyUser.objects.all()
    return render(request, 'Admin/BlockedAccounts.html', {'blocked_accounts': blocked_accounts})


def create_block(request, id_user):
    if request.method == 'POST':
        form = CreateBlock(request.POST)

        if form.is_valid():
            reason = form.cleaned_data['reason_block']
            user = models.MyUser.objects.get(id=id_user)
            user.reason_block = reason
            user.is_active = 0
            user.save()
            mes = user.username + " заблокирован"
            return render(request, 'Admin/Done.html', {'message': mes})
    else:
        form = CreateBlock()

    return render(request, 'Admin/CreateBlock.html', {'form': form})


def search_by_id(request):
    if request.method == 'POST':
        form = SearchId(request.POST)

        if form.is_valid():
            user_id = form.cleaned_data['field_id']
            results = models.MyUser.objects.get(id=user_id)
            return render(request, 'Search/SearchById.html', {'form': form, 'results': results})
    else:
        form = SearchId()
        return render(request, "Search/SearchById.html", {'form': form})


def edit_user_admin(request, id_user):
    user_for_edit = models.MyUser.objects.get(id=id_user)

    class EditUserAdmin(forms.Form):
        email = forms.CharField(label="Почтовый адрес", max_length=50, required=True, initial=user_for_edit.email)
        name = forms.CharField(label="Ваше имя", max_length=50, required=True, initial=user_for_edit.name)
        surname = forms.CharField(label="Ваша фамилия", max_length=50, required=True, initial=user_for_edit.surname)
        last_name = forms.CharField(label="Ваше отчество", max_length=50, required=True, initial=user_for_edit.last_name)
        age = forms.IntegerField(label="Ваш возраст", required=True, initial=user_for_edit.age)
        passport_id = forms.CharField(label="Номер вашего паспорта", max_length=50, required=True,
                                      initial=user_for_edit.passport_id)
        phone = forms.CharField(label="Ваш номер телефона", max_length=50, required=True, initial=user_for_edit.phone)
        address = forms.CharField(label="Ваш адрес", max_length=50, required=True, initial=user_for_edit.address)

    if request.method == 'POST':
        form = EditUserAdmin(request.POST)

        if form.is_valid():
            user = models.MyUser.objects.get(id=id_user)
            user.email = form.cleaned_data['email']
            user.name = form.cleaned_data['name']
            user.surname = form.cleaned_data['surname']
            user.last_name = form.cleaned_data['last_name']
            user.age = form.cleaned_data['age']
            user.passport_id = form.cleaned_data['passport_id']
            user.phone = form.cleaned_data['phone']
            user.address = form.cleaned_data['address']
            user.save()
            mes = "Личные данные пользователя " + user.username + " успешно изменены и сохранены"
            return render(request, 'Admin/Done.html', {'message': mes})

    else:
        form = EditUserAdmin()
    return render(request, "Admin/EditUser.html", {'form': form})