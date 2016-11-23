from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, username, name, surname, last_name, age, passport_id, phone, address, email,
                    taxpayer_account_number, license_field, ie, password=None):
        if ie:
            user = self.model(
                username=username,
                name=name,
                surname=surname,
                last_name=last_name,
                age=age,
                passport_id=passport_id,
                phone=phone,
                address=address,
                email=self.normalize_email(email),
                taxpayer_account_number=taxpayer_account_number,
                license_field=license_field,
                ie=ie,
            )
        else:
            user = self.model(
                username=username,
                name=name,
                surname=surname,
                last_name=last_name,
                age=age,
                passport_id=passport_id,
                phone=phone,
                address=address,
                email=self.normalize_email(email),
                ie=ie,
                taxpayer_account_number=None,
                license_field=None,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, surname, last_name, age, passport_id, phone, address, email, password):
        user = self.model(
            username=username,
            name=name,
            surname=surname,
            last_name=last_name,
            age=age,
            passport_id=passport_id,
            phone=phone,
            address=address,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(verbose_name='Логин', max_length=50, unique=True)
    password = models.CharField(verbose_name='Пароль', max_length=50)
    name = models.CharField(verbose_name='Имя', max_length=50)
    surname = models.CharField(verbose_name='Фамилия', max_length=50)
    last_name = models.CharField(verbose_name='Отчество', max_length=50)
    age = models.IntegerField(verbose_name='Возраст')
    passport_id = models.CharField(verbose_name='Номер паспорта', max_length=50)
    phone = models.CharField(verbose_name='Телефон', max_length=50)
    address = models.CharField(verbose_name='Адрес', max_length=50)
    email = models.CharField(verbose_name='Электронная почта', max_length=50)
    taxpayer_account_number = models.IntegerField(verbose_name='УНН', null=True)
    license_field = models.CharField(verbose_name='Лицензия', max_length=50, null=True)
    ie = models.BooleanField(verbose_name='ИП', default=False)
    balance = models.FloatField(null=True, default=0)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'surname', 'last_name', 'age', 'passport_id', 'phone', 'address', 'email', 'ie']

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def get_full_name(self):
        return self.Login

    def get_short_name(self):
        return self.Login

    def getId(self):
        return str(self.id)


class Rent(models.Model):
    name = models.CharField(verbose_name='Название', max_length=50)
    address = models.CharField(verbose_name='Адрес', max_length=50)
    min_rent_time = models.IntegerField(verbose_name='Срок аренды')
    area = models.IntegerField(verbose_name='Площадь', )
    date_of_construction = models.IntegerField(verbose_name='Год строительства', default=None)
    creation_date = models.DateField(default=None)
    other = models.CharField(verbose_name='Другое', max_length=100)
    cost = models.CharField(verbose_name='Цена аренды', max_length=50)
    user_login = models.CharField(verbose_name="hide", max_length=50, null=True)

    def getId(self):
        return str(self.id)

    def getUserLogin(self):
        return str(self.user_login)