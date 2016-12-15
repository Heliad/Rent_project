from TOFI import models


class Transaction(object):
    def __init__(self, amount, tr_from, tr_to, is_monetize=False):
        self.tr_from = tr_from
        self.tr_to = tr_to
        self.amount = float(amount)
        self.is_monetize = is_monetize
        self.mon_value = models.Monetization.objects.get(id=1).value_mon

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

        result = Check(tr_from=self.tr_from, tr_to=self.tr_to, amount=self.amount, is_monetize=self.is_monetize).check()

        if type(result) == str:
            return False, result

        if result[0]:
            self.tr_from.size -= self.amount
            if self.is_monetize:
                self.tr_from.size -= self.amount * self.mon_value
        else:
            self.tr_from.balance -= self.amount
            if self.is_monetize:
                self.tr_from.balance -= self.amount * self.mon_value

        if result[1]:
            self.tr_to.size += self.amount
        else:
            self.tr_to.balance += self.amount

        if self.is_monetize:
            a_card = models.UserCard.objects.get(name_card_owner='Admin')
            a_card.size += self.amount * self.mon_value
            a_card.save()

        self.tr_from.save()
        self.tr_to.save()
        return True, 'Транзакция прошла успешно'


class Check(object):
    def __init__(self, num=None, validity=None, card_owner=None, cvc2_cvv=None, tr_from=None, tr_to=None, amount=None, is_monetize=False):
        self.num = num
        self.validity = validity
        self.card_owner = card_owner
        self.cvc2_cvv = cvc2_cvv
        self.tr_from = tr_from
        self.tr_to = tr_to
        self.amount = amount
        self.is_monetize = is_monetize

    def check(self):
        if not self.tr_from and not self.tr_to and not self.amount:
            return 'error'
        result = list()
        try:
            card = models.UserCard.objects.get(card_num=self.tr_from.card_num)
            if card.size < self.amount:
                return 'Недостаточно средств на карте'
            if self.is_monetize and card.size < self.amount + self.amount * models.Monetization.objects.get(
                    id=1).value_mon:
                return 'Недостаточно средств на карте'
            result.append(True)
        except:
            try:
                balance = models.MyUser.objects.get(username=self.tr_from.username)
                if balance.balance < self.amount:
                    return 'Недостаточно средств на счете'
                if self.is_monetize and balance.balance < self.amount + self.amount * models.Monetization.objects.get(
                        id=1).value_mon:
                    return 'Недостаточно средств на карте'
                result.append(False)
            except:
                return 'Введены неверные данные'
        try:
            models.UserCard.objects.get(card_num=self.tr_to.card_num)
            result.append(True)
        except:
            try:
                models.MyUser.objects.get(username=self.tr_to.username)
                result.append(False)
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
