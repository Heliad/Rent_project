import datetime

from TOFI import models


class Transaction(object):
    def __init__(self, amount, tr_from, tr_to, is_monetize=False):
        self.tr_from = tr_from
        self.tr_to = tr_to
        self.amount = float(amount)
        self.is_monetize = is_monetize
        self.mon_value = models.Monetization.objects.get(id=1).value_mon
        self.currency = dict()
        for i in models.Currency.objects.all():
            self.currency.update({i.currency_name: i.currency_value})
        self.currency.update({'BYN': 1})

    def make_transaction(self):

        if type(self.tr_from) == str:
            try:
                int(self.tr_from)
                self.tr_from = models.UserCard.objects.get(card_num=self.tr_from)
            except:
                self.tr_from = models.MyUser.objects.get(username=self.tr_from)

        if type(self.tr_to) == str:
            try:
                int(self.tr_to)
                self.tr_to = models.UserCard.objects.get(card_num=self.tr_to)
            except:
                self.tr_to = models.MyUser.objects.get(username=self.tr_to)

        result = Check(tr_from=self.tr_from, tr_to=self.tr_to, amount=self.amount,
                       is_monetize=self.is_monetize, currency=self.currency).check()

        if type(result) == str:
            return False, result

        if result[0][0]:
            self.tr_from.size -= self.amount / self.currency.get(self.tr_from.currency_type)
            if self.is_monetize:
                self.tr_from.size -= self.amount * self.mon_value / self.currency.get(self.tr_from.currency_type)
        elif not result[0][0]:
            self.tr_from.balance -= self.amount
            if self.is_monetize:
                self.tr_from.balance -= self.amount * self.mon_value

        if result[1][0]:
            self.tr_to.size += self.amount / self.currency.get(self.tr_to.currency_type)
        elif not result[1][0]:
            self.tr_to.balance += self.amount

        if self.is_monetize:
            a_card = models.UserCard.objects.get(name_card_owner='Admin')
            a_card.size += self.amount * self.mon_value / self.currency.get(a_card.currency_type)
            a_card.save()

        self.tr_from.save()
        self.tr_to.save()
        return True, 'Транзакция прошла успешно'


class Check(object):
    def __init__(self, num=None, validity=None, card_owner=None, cvc2_cvv=None,
                 tr_from=None, tr_to=None, amount=None, is_monetize=False, currency=None):
        self.num = num
        self.validity = validity
        self.card_owner = card_owner
        self.cvc2_cvv = cvc2_cvv
        self.tr_from = tr_from
        self.tr_to = tr_to
        self.amount = amount
        self.is_monetize = is_monetize
        self.currency = currency

    def check(self):
        if not self.tr_from and not self.tr_to and not self.amount:
            return 'error'
        result = list()
        try:
            card = models.UserCard.objects.get(card_num=self.tr_from.card_num)
            if card.size < self.amount / self.currency.get(card.currency_type):
                return 'Недостаточно средств на карте'
            if self.is_monetize and card.size < (self.amount + self.amount * models.Monetization.objects.get(
                    id=1).value_mon) / self.currency.get(card.currency_type):
                return 'Недостаточно средств на карте'
            result.append([True, card.currency_type])
        except:
            try:
                balance = models.MyUser.objects.get(username=self.tr_from.username)
                if balance.balance < self.amount:
                    return 'Недостаточно средств на счете'
                if self.is_monetize and balance.balance < self.amount + self.amount * models.Monetization.objects.get(
                        id=1).value_mon:
                    return 'Недостаточно средств на карте'
                result.append([False, 'BYN'])
            except:
                return 'Введены неверные данные'
        try:
            models.UserCard.objects.get(card_num=self.tr_to.card_num)
            result.append([True, self.tr_to.currency_type])
        except:
            try:
                models.MyUser.objects.get(username=self.tr_to.username)
                result.append([False, 'BYN'])
            except:
                return 'Карты с таким номером не существует'
        return result

    def check_card(self):
        try:
            models.UserCard.objects.get(card_num=self.num, period_validity=self.validity,
                                        name_card_owner=self.card_owner, CVC2_CVV=self.cvc2_cvv)
            return True
        except:
            return False


class PaymentManager(object):
    def __init__(self, size, rent):
        self.rent = rent
        self.size = size
        self.size = float(self.size)
        self.cost = float(self.rent.cost)
        self.payed = float(self.rent.payed_until_time)

    def run(self):
        if self.rent.fine > 0:
            if self.size <= self.rent.fine:
                self.rent.fine -= self.size
                self.size = 0
            else:
                self.size -= self.rent.fine
                self.rent.fine = 0
        interval = models.Rent.objects.get(id=self.rent.id_house.id).payment_interval
        if self.size == self.cost - self.payed:
            self.rent.next_payment_date += datetime.timedelta(days=interval)
            self.rent.payed_until_time = 0
        elif self.size < self.cost - self.payed:
            self.rent.payed_until_time += self.size
        elif self.size > self.cost - self.payed:
            o = self.size / self.cost
            self.rent.next_payment_date += datetime.timedelta(days=interval * int(o))
            self.rent.payed_until_time = self.size - (self.cost * int(o)) + self.payed
            if self.rent.payed_until_time >= self.cost:
                self.rent.payed_until_time -= self.cost
                self.rent.next_payment_date += datetime.timedelta(days=interval)
        self.rent.save()
