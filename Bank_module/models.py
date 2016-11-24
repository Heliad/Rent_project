from django.db import models


class UserCard(models.Model):
    card_num = models.CharField(verbose_name="Номер карты/Card number", max_length=16)
    period_validity = models.CharField(verbose_name="Срок действия (ММГГ)", max_length=5)
    name_card_owner = models.CharField(verbose_name="Имя держателя карты", max_length=50)
    CVC2_CVV = models.CharField(verbose_name="CVC2/CVV", max_length=3)
    size = models.IntegerField(verbose_name='Баланс')
