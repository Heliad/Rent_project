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