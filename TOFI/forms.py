from django import forms
from django.core.validators import *
from django.forms import SelectDateWidget

from .models import MyUser, Rent, AddImage


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', max_length=50, min_length=10, widget=forms.PasswordInput,
                               validators=[RegexValidator('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$')])
    password1 = forms.CharField(label='Подтвержение пароля', max_length=50, min_length=10, widget=forms.PasswordInput)

    name = forms.CharField(label='Имя:', required=True, validators=[RegexValidator('^[а-яА-Я]*$')])
    surname = forms.CharField(label='Фамилия:', required=True, validators=[RegexValidator('^[а-яА-Я]*$')])
    last_name = forms.CharField(label='Отчество:', required=True, validators=[RegexValidator('^[а-яА-Я]*$')])
    age = forms.IntegerField(label='Возраст:', validators=[MaxValueValidator(100), MinValueValidator(18)])

    email = forms.CharField(label='Email:', validators=[EmailValidator()])
    phone = forms.CharField(label='Телефон:', help_text='Необходимо ввести номер с кодом страны и оператора',
                            validators=[RegexValidator('^\+[0-9\-\ ]*$')])
    address = forms.CharField(label='Адрес:', max_length=50, validators=[RegexValidator('^[0-9а-яА-Я/./,/;/ /-]*$')])
    passport_id = forms.CharField(label='Номер пасспорта:', max_length='50')

    ie = forms.BooleanField(label='ИП', widget=forms.CheckboxInput(attrs={'onchange': "onChange()"}),
                            required=False, initial=True)
    taxpayer_account_number = forms.IntegerField(label='УНН', required=False)
    license_field = forms.CharField(label='Лицензия', required=False)

    class Meta:
        model = MyUser
        fields = ['username', 'password', 'password1', 'passport_id', 'email',
                  'name', 'surname', 'last_name', 'age', 'phone', 'address',
                  'ie', 'taxpayer_account_number', 'license_field']


class RentForm(forms.ModelForm):
    name = forms.CharField(label='Имя:', required=True,
                           validators=[RegexValidator('^[а-яА-Я]*$')])
    address = forms.CharField(label='Адрес:', max_length=50, validators=[RegexValidator('^[0-9а-яА-Я/./,/;/ /-]*$')])
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
                                          validators=[MinValueValidator(1), MaxValueValidator(30)])

    class Meta:
        model = Rent
        fields = ['name', 'address', 'min_rent_time', 'area', 'date_of_construction', 'cost', 'payment_interval']


class RefillBalance(forms.Form):
    card_num = forms.CharField(label="Номер карты/Card number:", max_length=16, min_length=16,
                               required=True, validators=[RegexValidator('^[0-9]*$')])
    period_validity = forms.CharField(label="Срок действия (ММ/ГГ):", max_length=5, min_length=5,
                                      required=True, validators=[RegexValidator('^[0-9]{2,2}/{1,1}[0-9]*$')],
                                      widget=forms.TextInput(attrs={'placeholder': 'ММ/ГГ'}))
    name_card_owner = forms.CharField(label="Имя держателя карты:", max_length=50, required=True,
                                      validators=[RegexValidator('^[a-zA-Z\ ]*$')])
    CVC2_CVV = forms.CharField(label="CVC2/CVV:", max_length=3, min_length=3, required=True,
                               validators=[RegexValidator('^[0-9]*$')])
    size = forms.IntegerField(label="Сумма:", required=True,
                              validators=[MinValueValidator(10), MaxValueValidator(1000000)])


class ChangePassword(forms.Form):
    old_password = forms.CharField(label="Старый пароль:", max_length=50, required=True)
    new_password = forms.CharField(label="Новый пароль:", max_length=50, required=True)
    new_password_repeat = forms.CharField(label="Повторите пароль:", max_length=50, required=True)


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


class SearchId(forms.Form):
    field_id = forms.IntegerField(label="Введите id пользователя:")


class RejectRent(forms.Form):
    reject_reason = forms.CharField(label="Укажите причину отказа:", max_length=100)


class ExtractBalance(forms.Form):
    YEARS_START = ('2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017')
    period_start = forms.DateField(label="Начало периода:", widget=SelectDateWidget(years=YEARS_START), required=True)
    period_end = forms.DateField(label="Конец периода:", widget=SelectDateWidget, required=True)


class CreateBlock(forms.ModelForm):
    reason_block = forms.CharField(label='Причина блокировки:', max_length=100)

    class Meta:
        model = MyUser
        fields = ['reason_block']


class EditPenalty(forms.Form):
    kind_penalty = forms.CharField(label="Название:", required=True, max_length=50)
    describe_penalty = forms.CharField(label="Описание:", required=True, max_length=150, widget=forms.Textarea)
    cost_penalty = forms.FloatField(label="Размер штрафа:", required=True)


class AddImageForm(forms.ModelForm):

    class Meta:
        model = AddImage
        fields = ['image', 'name', 'describe']
