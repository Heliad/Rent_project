from django import forms
from django.forms import SelectDateWidget
from .models import MyUser, Rent


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Подтвержение пароля', widget=forms.PasswordInput)
    ie = forms.BooleanField(label='ИП', widget=forms.CheckboxInput)

    # license_field = forms.Textarea()
    ie.required = False
    taxpayer_account_number = forms.IntegerField(label='УНН')
    taxpayer_account_number.required = False
    license_field = forms.CharField(label='Лицензия')
    license_field.required = False

    class Meta:
        model = MyUser
        fields = ['username', 'password', 'password1', 'email', 'name',
                  'surname', 'last_name', 'age', 'passport_id', 'phone', 'address', 'ie', 'taxpayer_account_number',
                  'license_field']


class RentForm(forms.ModelForm):

    other = forms.CharField(label="Другое:", max_length=100, required=True,
                            widget=forms.Textarea(attrs={'placeholder': 'Введите описание дома...', 'rows': '4'}))

    class Meta:
        model = Rent
        fields = ['name', 'address', 'min_rent_time', 'area', 'date_of_construction', 'cost']


class RefillBalance(forms.Form):
    card_num = forms.CharField(label="Номер карты/Card number", max_length=16, required=True)
    period_validity = forms.CharField(label="Срок действия (ММГГ)", max_length=5, required=True)
    name_card_owner = forms.CharField(label="Имя держателя карты", max_length=50, required=True)
    CVC2_CVV = forms.CharField(label="CVC2/CVV", max_length=3, required=True)
    size = forms.IntegerField(label="Сумма", required=True)


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
