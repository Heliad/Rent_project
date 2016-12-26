import datetime

from django import forms
from django.core.validators import *

from .models import MyUser, Rent, AddImage


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', max_length=50, min_length=10, widget=forms.PasswordInput,
                               validators=[RegexValidator('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$')])
    password1 = forms.CharField(label='Подтвержение пароля', max_length=50, min_length=10, widget=forms.PasswordInput)

    name = forms.CharField(label='Имя:', required=True, validators=[RegexValidator('^[а-яА-Я]*$')], initial='рапрап')
    surname = forms.CharField(label='Фамилия:', required=True, validators=[RegexValidator('^[а-яА-Я]*$')], initial='рапрап')
    last_name = forms.CharField(label='Отчество:', required=True, validators=[RegexValidator('^[а-яА-Я]*$')], initial='рапрап')
    age = forms.IntegerField(label='Возраст:', validators=[MaxValueValidator(110), MinValueValidator(18)], initial=22)

    email = forms.CharField(label='Email:', max_length=50, validators=[EmailValidator()])
    phone = forms.CharField(label='Телефон:', max_length=50, validators=[RegexValidator('^\+[0-9\-\ ]*$')])
    address = forms.CharField(label='Адрес:', max_length=50, validators=[RegexValidator('^[0-9а-яА-Я/./,/;/ /-]*$')], initial='рапрап')
    passport_id = forms.CharField(label='Номер паспорта:', max_length='9', min_length=9, required=True,
                                  validators=[RegexValidator('^(АВ|ВМ|НВ|КН|МР|МС|КВ|РР|МН)[0-9]{7,7}$')], initial='АВ3534534')

    ie = forms.BooleanField(label='ИП', widget=forms.CheckboxInput(attrs={'onchange': "onChange()"}),
                            required=False, initial=False)
    taxpayer_account_number = forms.IntegerField(label='УНН:', required=False,
                                                 validators=[MinValueValidator(1), MaxValueValidator(100000)])
    license_field = forms.CharField(label='Лицензия:', required=False,
                                    validators=[RegexValidator('^[0-9а-яА-ЯёЁa-zA-Z/./,/;/ /-]*$')])

    class Meta:
        model = MyUser
        fields = ['username', 'password', 'password1', 'passport_id', 'email',
                  'name', 'surname', 'last_name', 'age', 'phone', 'address',
                  'ie', 'taxpayer_account_number', 'license_field']


class RentForm(forms.ModelForm):
    name = forms.CharField(label='Имя:', required=True,
                           validators=[RegexValidator('^[а-яА-Я]*$')])
    address = forms.CharField(label='Адрес:', max_length=50,
                              validators=[RegexValidator('^[0-9а-яА-Я/./,/;/ /-]*$')])
    other = forms.CharField(label="Описание дома:", max_length=100, required=True,
                            widget=forms.Textarea(attrs={'placeholder': 'Введите описание дома...', 'rows': '4'}),
                            validators=[RegexValidator('^[0-9а-яА-Я/./,/;/ /-]*$')])
    min_rent_time = forms.IntegerField(label="Время аренды:", required=True,
                                       validators=[MinValueValidator(1), MaxValueValidator(365)])
    area = forms.IntegerField(label="Жилая площадь(кв.м.):", required=True,
                              validators=[MinValueValidator(3), MaxValueValidator(1000)])
    date_of_construction = forms.IntegerField(label="Год постройки:", required=True,
                                              validators=[MinValueValidator(1950), MaxValueValidator(2020)])
    cost = forms.IntegerField(label="Цена:", required=True,
                              validators=[MinValueValidator(1), MaxValueValidator(1000000)])
    payment_interval = forms.IntegerField(label="Интервал оплаты:", required=True,
                                          validators=[MinValueValidator(1), MaxValueValidator(365)])

    class Meta:
        model = Rent
        fields = ['name', 'address', 'min_rent_time', 'area', 'date_of_construction', 'cost', 'payment_interval']


class RefillBalance(forms.Form):
    card_num = forms.CharField(label="Номер карты:", max_length=16, min_length=16, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control height70'}),
                               validators=[RegexValidator('^[0-9]*$')])
    period_validity = forms.CharField(label="Срок действия (ММ/ГГ)", max_length=5, min_length=5, required=True,
                                      validators=[RegexValidator('^[0-9]{2,2}/{1,1}[0-9]*$')],
                                      widget=forms.TextInput(attrs={'placeholder': 'ММ/ГГ',
                                                                    'class': 'form-control height70'}))
    name_card_owner = forms.CharField(label="Имя держателя карты:", max_length=50, min_length=3, required=True,
                                      widget=forms.TextInput(attrs={'class': 'form-control height70'}),
                                      validators=[RegexValidator('^[a-zA-Z\ ]*$')])
    CVC2_CVV = forms.CharField(label="CVC2/CVV:", max_length=3, min_length=3, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control height70'}),
                               validators=[RegexValidator('^[0-9]*$')])
    size = forms.IntegerField(label="Сумма:", required=True, validators=[MaxValueValidator(1000000),
                                                                         MinValueValidator(10)])


class ChangePassword(forms.Form):
    old_password = forms.CharField(label="Старый пароль:", max_length=50, required=True,
                                   widget=forms.PasswordInput)
    new_password = forms.CharField(label="Новый пароль:", max_length=50, min_length=10, required=True,
                                   widget=forms.PasswordInput,
                                   validators=[RegexValidator('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$')])
    new_password_repeat = forms.CharField(label="Повторите пароль:", max_length=50, min_length=10, required=True,
                                          widget=forms.PasswordInput,
                                          validators=[RegexValidator('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$')])


class DeleteMySelf(forms.Form):
    password = forms.CharField(label="Введите пароль:", max_length=50, required=True)


class AddComment(forms.Form):
    text_comment = forms.CharField(label="Введите отзыв", max_length=50, required=True)


class SearchRent(forms.Form):
    TYPE_SEARCH = (('1', 'Поиск по диапозону цен'), ('2', 'Поиск по названию'),
                   ('3', 'Поиск по логину арендатора'), ('4', 'Поиск по размеру площади'))

    type_search = forms.ChoiceField(widget=forms.RadioSelect, choices=TYPE_SEARCH, label="Критерий поиска:")
    min_interval = forms.IntegerField(label="Минимальная цена:", required=False)
    max_interval = forms.IntegerField(label="Максимальная цена:", required=False)
    login_or_name_rent = forms.CharField(label="Название дома или логин арендатора:", required=False)
    square = forms.IntegerField(label="Площадь:", required=False)


class SearchUser(forms.Form):
    TYPE_SEARCH = (('1', 'Поиск по логину'), ('2', 'Поиск по фамилии'), ('3', 'Поиск по Email'))

    type_search = forms.ChoiceField(widget=forms.RadioSelect, choices=TYPE_SEARCH, label="Критерий поиска:")
    field_search = forms.CharField(label="Введите информацию о пользователе:", max_length=50)


class RejectRent(forms.Form):
    reject_reason = forms.CharField(label="Укажите причину отказа:", max_length=100)


class ExtractBalance(forms.Form):
    period_start = forms.DateField(input_formats=['%d/%m/%Y'], label="Начало периода:",
                                   widget=forms.DateInput(attrs={'class': 'datetime'}), required=True)
    period_end = forms.DateField(input_formats=['%d/%m/%Y'], label="Конец периода:",
                                 widget=forms.DateInput(attrs={'class': 'datetime'}), required=True,
                                 initial=datetime.date.today().strftime('%d/%m/%Y'))


class CreateBlock(forms.ModelForm):
    reason_block = forms.CharField(label='Причина блокировки:', max_length=100)

    class Meta:
        model = MyUser
        fields = ['reason_block']


class EditPenalty(forms.Form):
    kind_penalty = forms.CharField(label="Название:", required=True, max_length=50, min_length=5,
                                   validators=[RegexValidator('^[а-яёЁА-Я\ ]*$')])
    describe_penalty = forms.CharField(label="Описание:", required=True, max_length=150, min_length=5,
                                       validators=[RegexValidator('^[а-яЁёА-Я0-9\.\,\(\)\; ]*$')],
                                       widget=forms.Textarea)
    cost_penalty = forms.FloatField(label="Размер штрафа:", required=True, min_value=0,
                                    validators=[RegexValidator('^[0-9]{1,6}(,|.){1,1}[0-9]{1,2}$')])


class AddImageForm(forms.ModelForm):

    class Meta:
        model = AddImage
        fields = ['image', 'name', 'describe']
