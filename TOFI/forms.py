from django import forms
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

    class Meta:
        model = Rent
        fields = ['name', 'address', 'min_rent_time', 'area', 'date_of_construction', 'other', 'cost']


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

