from django.core import management
from django.http import HttpResponseRedirect
from django.shortcuts import render

from TOFI import models
from TOFI import transaction as t
from .forms import *


def main_admin(request):
    if request.user.is_anonymous or not request.user.is_admin:
        return HttpResponseRedirect("/login")

    return render(request, 'Admin/MainAdmin.html')


def blocked_accounts(request):
    if request.user.is_anonymous or not request.user.is_admin and not request.user.is_moder:
        return HttpResponseRedirect("/login")

    blocked_accounts = models.MyUser.objects.all().exclude(is_admin=True)
    return render(request, 'Admin/BlockedAccounts.html', {'blocked_accounts': blocked_accounts})


def create_block(request, id_user):
    if request.user.is_anonymous or not request.user.is_admin and not request.user.is_moder:
        return HttpResponseRedirect("/login")

    if request.method == 'POST':
        form = CreateBlock(request.POST)

        if form.is_valid():
            reason = form.cleaned_data['reason_block']
            user = models.MyUser.objects.get(id=id_user)
            user.reason_block = reason
            user.is_active = 0
            user.wrong_password_number = 0
            user.save()
            mes = user.username + " заблокирован."
            return render(request, 'Admin/Done.html', {'message': mes})
    else:
        form = CreateBlock()

    return render(request, 'Admin/CreateBlock.html', {'form': form})


def delete_block(request, id_user):
    if request.user.is_anonymous or not request.user.is_admin and not request.user.is_moder:
        return HttpResponseRedirect("/login")

    user = models.MyUser.objects.get(id=id_user)
    user.reason_block = ''
    user.is_active = 1
    user.save()
    mes = "Пользователь " + user.username + " разблокирован"
    return render(request, 'Admin/Done.html', {'message': mes})


def search_by_id(request):

    class SearchId(forms.Form):
        field_id = forms.IntegerField(label="Введите Id пользователя:", required=True, min_value=1, max_value=1000000)

    results, no_rez = None, ''
    if request.method == 'POST':
        form = SearchId(request.POST)

        if form.is_valid():
            user_id = form.cleaned_data['field_id']
            try:
                results = models.MyUser.objects.get(id=user_id)
            except:
                pass

            if results is None:
                no_rez = 'Поиск не дал результатов...'
            return render(request, 'Search/SearchById.html', {'form': form, 'results': results, 'no_rez': no_rez})
    else:
        form = SearchId()
        return render(request, "Search/SearchById.html", {'form': form})


def edit_user_admin(request, id_user):
    if request.user.is_anonymous or not request.user.is_admin and not request.user.is_moder:
        return HttpResponseRedirect("/login")

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
        passport_id = forms.CharField(label='Номер паспорта:', max_length='9', min_length=9, required=True,
                                      validators=[RegexValidator('^(АВ|ВМ|НВ|КН|МР|МС|КВ|РР|МН)[0-9]{7,7}$')],
                                      initial=user_for_edit.passport_id)
        phone = forms.CharField(label="Ваш номер телефона:", max_length=50, required=True, initial=user_for_edit.phone,
                                validators=[RegexValidator('^\+[0-9\-\ ]*$')])
        address = forms.CharField(label="Ваш адрес:", max_length=50, required=True, initial=user_for_edit.address,
                                  validators=[RegexValidator('^[0-9а-яА-Я/./,/;/ /-]*$')])
        balance = forms.FloatField(label="Баланс:", required=True, initial=user_for_edit.balance,
                                   validators=[RegexValidator('^[0-9]{1,6}(,|.){1,1}[0-9]{1,2}$')])
        is_moder = forms.BooleanField(label="Модератор:", initial=user_for_edit.is_moder, required=False)

    if request.method == 'POST':
        form = EditUserAdmin(request.POST)

        if form.is_valid():
            user = models.MyUser.objects.get(id=id_user)
            list_users = models.MyUser.objects.all()
            for us in list_users:
                if us.email == form.cleaned_data['email']:
                    if us.username != user.username:
                        error = "Пользователь с таким почтовым адресом уже зарегистрирован"
                        return render(request, "Admin/EditUser.html", {'form': form, 'error': error})
                if us.passport_id == form.cleaned_data['passport_id']:
                    if us.username != user.username:
                        error = "Пользователь с таким номером пасспорта уже зарегистрирован"
                        return render(request, "Admin/EditUser.html", {'form': form, 'error': error})

            user.email = form.cleaned_data['email']
            user.name = form.cleaned_data['name']
            user.surname = form.cleaned_data['surname']
            user.last_name = form.cleaned_data['last_name']
            user.age = form.cleaned_data['age']
            user.passport_id = form.cleaned_data['passport_id']
            user.phone = form.cleaned_data['phone']
            user.address = form.cleaned_data['address']
            user.balance = form.cleaned_data['balance']
            mes = "Личные данные пользователя " + user.username + " успешно изменены и сохранены. "
            if form.cleaned_data['is_moder']:
                if not user.ie:
                    doned_rents = models.DoneRent.objects.all().filter(id_user_renter=user.id)
                    if not doned_rents:
                        user.is_moder = form.cleaned_data['is_moder']
                    else:
                        mes += "Но пользователь " + user.username + " не может быть модератором, " \
                                                                    "т.к. арендует дом."
                else:
                    mes += "Но пользователь " + user.username + " не может быть модератором, " \
                                                                "т.к. является арендодатором."
            else:
                user.is_moder = False
            user.save()
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
            if 'passport_id' in err:
                error = 'Недопустимые значение в поле Номер пасспорта!'
            if 'balance' in err:
                error = 'Недопустимые значение в поле Баланс(Пример: XXX,XX)!'

    else:
        form = EditUserAdmin()
    return render(request, "Admin/EditUser.html", {'form': form, 'id_user': user_for_edit.id, 'error': error})


def all_currency(request):
    if request.user.is_anonymous or not request.user.is_admin:
        return HttpResponseRedirect("/login")

    cur = models.Currency.objects.all()
    return render(request, "Admin/AllCurrency.html", {'cur': cur})


def edit_currency(request, id_cur):
    if request.user.is_anonymous or not request.user.is_admin:
        return HttpResponseRedirect("/login")

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
    if request.user.is_anonymous or not request.user.is_admin:
        return HttpResponseRedirect("/login")

    error = ''
    mon = models.Monetization.objects.get(id=1)

    class Monet(forms.Form):
        describe_mon = forms.CharField(label="Описание:", required=True, max_length=150, min_length=5,
                                       initial=mon.describe_mon, widget=forms.Textarea(attrs={'rows': '3'}))
        value_mon = forms.FloatField(label="Размер:", required=True, initial=mon.value_mon,
                                     validators=[RegexValidator('^[0-9]{1,6}(,|.){1,1}[0-9]{1,2}$')])

    if request.method == 'POST':
        form = Monet(request.POST)

        if form.is_valid():
            mon.describe_mon = form.cleaned_data['describe_mon']
            mon.value_mon = form.cleaned_data['value_mon']
            mon.save()

            mes = 'Изменения приняты и сохранены'
            return render(request, 'Admin/Done.html', {'message': mes})

        else:
            err = form.errors.as_data()
            if 'value_mon' in err:
                error = 'Недопустимые значение в поле Размер(Пример: XX,XXX)!'
    else:
        form = Monet()

    return render(request, 'Admin/Monetization.html', {'form': form, 'error': error})


def refill_balance_admin(request, id_user):
    if request.user.is_anonymous or not request.user.is_admin and not request.user.is_moder:
        return HttpResponseRedirect("/login")

    error = ''
    if request.method == 'POST':
        form = RefillBalance(request.POST)

        if form.is_valid():
            card_num = form.cleaned_data['card_num']
            period_validity = form.cleaned_data['period_validity']
            name_card_owner = form.cleaned_data['name_card_owner']
            CVC2_CVV = form.cleaned_data['CVC2_CVV']
            size = form.cleaned_data['size']
            user = models.MyUser.objects.get(id=id_user)

            if t.Check(card_num, period_validity, name_card_owner, CVC2_CVV).check_card():
                c, m = t.Transaction(size, card_num, user).make_transaction()

                # Логирование операции пополнения баланса
                models.LogOperationsBalance.objects.create(id_user=request.user.id, type_operation='Пополнение баланса',
                                                           describe_operation="Баланс успешно пополнен на " + str(
                                                               size) + " BYN",
                                                           date_operation=datetime.date.today())
                if c:
                    mes = request.user.name + ", баланс пользователя " + user.username + ", успешно пополнен на " + str(size) + " BYN."
                else:
                    mes = m
                return render(request, 'Admin/Done.html', {'message': mes})
            else:
                return render(request, 'Admin/Done.html', {'message': 'Введены неверные данные!'})

        else:
            err = form.errors.as_data()
            print(err)
            if 'card_num' in err:
                error = 'Номер карты должен содержать только цифры!'
            if 'period_validity' in err:
                error = 'Срок действия карты указан неверно!(Пример: 12/17)'
            if 'name_card_owner' in err:
                error = 'В поле Имя держателя карты введены недопустимые символы!'
            if 'CVC2_CVV' in err:
                error = 'В поле CVC2_CVV введены недопустимые символы!'
            if 'size' in err:
                error = 'Сумма может быть от 10 BYN до 1млн BYN!'

    else:
        form = RefillBalance()
    return render(request, "Admin/RefillBalanceAdmin.html", {'form': form, 'error': error})


def change_time(request):
    class ChangeTime(forms.Form):
        shift_time = forms.IntegerField(label='Кол-во дней:')

    if request.method == 'GET':
        form = ChangeTime()
        return render(request, 'Admin/ChangeTime.html', {'form': form})
    else:
        form = ChangeTime(request.POST)
        if form.is_valid():
            shift = form.cleaned_data['shift_time']
            for s in range(shift):
                start_shift_at_datetime(datetime.now() + timedelta(days=1))
                management.call_command('autopay')
            print(datetime.now())
            return HttpResponseRedirect('/mainadmin')
        else:
            return HttpResponseRedirect('/mainadmin')
