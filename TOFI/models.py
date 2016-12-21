from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.db import models


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


class UserCard(models.Model):
    card_num = models.CharField(verbose_name="Номер карты/Card number", max_length=16)
    period_validity = models.CharField(verbose_name="Срок действия (ММГГ)", max_length=5)
    name_card_owner = models.CharField(verbose_name="Имя держателя карты", max_length=50)
    CVC2_CVV = models.CharField(verbose_name="CVC2/CVV", max_length=3)
    size = models.FloatField(verbose_name='Баланс')


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
    email = models.CharField(verbose_name='Электронная почта', max_length=50, unique=True)
    taxpayer_account_number = models.IntegerField(verbose_name='УНН', null=True)
    license_field = models.CharField(verbose_name='Лицензия', max_length=50, null=True)
    ie = models.BooleanField(verbose_name='ИП', default=False)
    balance = models.FloatField(verbose_name='', default=0)
    user_card_id = models.ManyToManyField(UserCard, default=None)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'surname', 'last_name', 'age', 'passport_id', 'phone', 'address', 'email', 'ie']

    is_active = models.BooleanField(default=True)
    reason_block = models.CharField(max_length=100, null=True)
    is_admin = models.BooleanField(default=False)
    is_moder = models.BooleanField(default=False)
    wrong_password_number = models.IntegerField(default=0)

    def get_full_name(self):
        return self.Login

    def get_short_name(self):
        return self.Login

    def getId(self):
        return str(self.id)


class Rent(models.Model):
    name = models.CharField(verbose_name='Название:', max_length=50)
    address = models.CharField(verbose_name='Адрес:', max_length=50)
    min_rent_time = models.IntegerField(verbose_name='Срок аренды:')
    area = models.IntegerField(verbose_name='Площадь:')
    payment_interval = models.IntegerField(verbose_name='Срок оплаты', default=None, null=True, blank=True)
    date_of_construction = models.IntegerField(verbose_name='Год строительства:', default=None)
    creation_date = models.DateField(default=None)
    other = models.CharField(verbose_name='Другое:', max_length=100)
    cost = models.CharField(verbose_name='Цена аренды:', max_length=50)
    user_login = models.ForeignKey(MyUser)
    status_rent = models.BooleanField(default=True)  # True - свободно, False - уже арендовано арендой

    def getId(self):
        return str(self.id)

    def getUserLogin(self):
        return str(self.user_login)


class MessageStatusRent(models.Model):
    id_user_from = models.IntegerField()
    login_user_from = models.CharField(max_length=50, null=True)
    id_user_to = models.IntegerField()
    creation_date = models.DateField(default=None)
    text_message = models.CharField(max_length=100)
    text_more = models.CharField(max_length=100)
    id_rent = models.IntegerField(null=True)
    is_new = models.BooleanField(default=True)  # прочитано ли сообщение
    is_done = models.BooleanField(default=False)  # запрос на аренду True - подтвердил
    type_mes = models.BooleanField(default=True)


class Comment(models.Model):
    text_comment = models.CharField(max_length=100)
    user_login = models.CharField(max_length=50)
    date_comment = models.DateField(default=None)


class CommentUser(models.Model):
    id_user_about = models.IntegerField()
    id_user_from = models.IntegerField()
    text_comment = models.CharField(max_length=50)
    date_comment = models.DateField(default=None)


class DoneRent(models.Model):
    id_house = models.ForeignKey(Rent)
    id_user_owner = models.ForeignKey(MyUser)
    id_user_renter = models.IntegerField()
    fine = models.FloatField(default=0)
    date_rent = models.DateField(default=None)
    payed_until_time = models.FloatField(default=0)
    cost = models.CharField(max_length=50)  # Цена одной платы
    next_payment_date = models.DateField(default=None)


class LogOperationsBalance(models.Model):  # Модель для логирования операций
    id_user = models.IntegerField()
    type_operation = models.CharField(max_length=50)  # Ввод/вывод/и т.д.
    describe_operation = models.CharField(max_length=100)  # Описание
    amount = models.IntegerField(default=0)
    date_operation = models.DateField(default=None)
    status = models.BooleanField(default=False)


class QuickPayment(models.Model):
    username = models.ForeignKey(MyUser)
    rent = models.ForeignKey(DoneRent)
    user_payment = models.CharField(max_length=50, default=None)
    amount = models.FloatField(default=None)


class Currency(models.Model):
    currency_name = models.CharField(max_length=10)
    currency_value = models.FloatField()


class Penalties(models.Model):  # Штрафы
    kind_penalty = models.CharField(max_length=50)
    describe_penalty = models.CharField(max_length=100)
    cost_penalty = models.FloatField()


class Monetization(models.Model):
    describe_mon = models.CharField(max_length=100)
    value_mon = models.FloatField()


class DonePenalty(models.Model):  # Назначенные штрафы
    describe_penalty = models.CharField(max_length=150)
    id_user_for = models.IntegerField()
    size_penalty = models.FloatField()
    id_done_rent = models.IntegerField()
    is_payd = models.BooleanField(default=False)


class AutoPayment(models.Model):
    quick_payment = models.ForeignKey(QuickPayment)
    next_payment_date = models.DateField(default=None)
    payment_interval = models.IntegerField(default=30)


class Complaint(models.Model):
    login_user_from = models.CharField(verbose_name="От кого жалоба:", max_length=100)
    login_user_to = models.CharField(verbose_name="На кого жалоба:", max_length=100)
    describe = models.CharField(verbose_name="Текст жалобы:", max_length=150)
    date = models.DateField(verbose_name="Дата подачи жалобы:", default=None)


class SessionKeys(models.Model):
    id_card = models.IntegerField()
    number_key = models.IntegerField()
    key = models.IntegerField()


class AddImage(models.Model):
    id_rent = models.IntegerField()
    image = models.ImageField(upload_to='imagesHouses/', height_field=None, width_field=None)
    name = models.CharField(verbose_name="Название:", max_length=100)
    describe = models.CharField(verbose_name="Описание:", max_length=150)


class AddImage2(models.Model):
    image = models.FileField(upload_to='imagesHouses/')
