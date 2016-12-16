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


def delete_block(request, id_user):
    user = models.MyUser.objects.get(id=id_user)
    user.reason_block = ''
    user.is_active = 1
    user.save()
    mes = "Пользователь " + user.username + " разблокирован"
    return render(request, 'Admin/Done.html', {'message': mes})


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
    error = ''
    user_for_edit = models.MyUser.objects.get(id=id_user)

    class EditUserAdmin(forms.Form):
        name = forms.CharField(label="Ваше имя:", max_length=50, required=True, initial=user_for_edit.name,
                               validators=[RegexValidator('^[а-яА-Я]*$')])
        surname = forms.CharField(label="Ваша фамилия:", max_length=50, required=True, initial=user_for_edit.surname,
                                  validators=[RegexValidator('^[а-яА-Я]*$')])
        last_name = forms.CharField(label="Ваше отчество:", max_length=50, required=True,
                                    initial=user_for_edit.last_name, validators=[RegexValidator('^[а-яА-Я]*$')])
        age = forms.IntegerField(label="Ваш возраст:", required=True, initial=user_for_edit.age,
                                 validators=[MaxValueValidator(100), MinValueValidator(18)])
        email = forms.CharField(label="Почтовый адрес:", max_length=50, required=True, initial=user_for_edit.email,
                                validators=[EmailValidator()])
        passport_id = forms.CharField(label="Номер вашего паспорта:", max_length=50, required=True,
                                      initial=user_for_edit.passport_id)
        phone = forms.CharField(label="Ваш номер телефона:", max_length=50, required=True, initial=user_for_edit.phone,
                                validators=[RegexValidator('^\+[0-9\-\ ]*$')])
        address = forms.CharField(label="Ваш адрес:", max_length=50, required=True, initial=user_for_edit.address,
                                  validators=[RegexValidator('^[0-9а-яА-Я/./,/;/ /-]*$')])
        balance = forms.FloatField(label="Баланс:", required=True, initial=user_for_edit.balance,
                                   validators=[RegexValidator('^[0-9]{1,6}(,|.){1,1}[0-9]{1,2}$')])

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
            user.balance = form.cleaned_data['balance']
            user.save()
            mes = "Личные данные пользователя " + user.username + " успешно изменены и сохранены"
            return render(request, 'Admin/Done.html', {'message': mes})
        else:
            err = form.errors.as_data()
            if 'phone' in err:
                error = 'Недопустимый номер телефона!'
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
            if 'balance' in err:
                error = 'Недопустимые значение в поле Баланс(Пример: XXX,XX)!'

    else:
        form = EditUserAdmin()
    return render(request, "Admin/EditUser.html", {'form': form, 'error': error})


def all_currency(request):
    cur = models.Currency.objects.all()
    return render(request, "Admin/AllCurrency.html", {'cur': cur})


def edit_currency(request, id_cur):
    cur = models.Currency.objects.get(id=id_cur)
    error = ''

    class EditCurrency(forms.Form):
        cur_name = forms.CharField(label="Наименование валюты:", max_length=3, min_length=3,
                                   required=True, initial=cur.currency_name,
                                   validators=[RegexValidator('^[A-Z]*$')])
        cur_value = forms.FloatField(label="Курс:", required=True, initial=cur.currency_value,
                                     validators=[RegexValidator('^[0-9]{1,6}(,|.){1,1}[0-9]{1,3}$')])

    if request.method == 'POST':
        form = EditCurrency(request.POST)

        if form.is_valid():
            cur.currency_name = form.cleaned_data['cur_name']
            cur.currency_value = form.cleaned_data['cur_value']
            cur.save()

            mes = "Информация о валюте с номером: " + str(cur.id) + " успешно изменена и сохранена"
            return render(request, 'Admin/Done.html', {'message': mes})
        else:
            err = form.errors.as_data()
            if 'cur_name' in err:
                error = 'В поле Название валюты недопустимые символы. Название должно ' \
                        'состоять из трех заглавных букв латинского алфавита.'
            if 'cur_value' in err:
                error = 'Недопустимые значение в поле Курс (Пример: XX,XXX)!'
    else:
        form = EditCurrency()
    return render(request, "Admin/EditCurrency.html", {'form': form, 'error': error})


def monetization(request):
    mon = models.Monetization.objects.get(id=1)

    class Monet(forms.Form):
        describe_mon = forms.CharField(label="Описание:", required=True, max_length=150,
                                           initial=mon.describe_mon, widget=forms.Textarea(attrs={'rows': '3'}))
        value_mon = forms.FloatField(label="Размер:", required=True, initial=mon.value_mon)

    if request.method == 'POST':
        form = Monet(request.POST)

        if form.is_valid():
            mon.describe_mon = form.cleaned_data['describe_mon']
            mon.value_mon = form.cleaned_data['value_mon']
            mon.save()

            mes = 'Изменения приняты и сохранены'
            return render(request, 'Admin/Done.html', {'message': mes})
    else:
        form = Monet()

    return render(request, 'Admin/Monetization.html', {'form': form})