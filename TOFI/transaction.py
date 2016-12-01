from TOFI import models


class Transaction(object):
    def __init__(self, amount, tr_from, tr_to):
        self.tr_from = tr_from
        self.tr_to = tr_to
        self.amount = int(amount)

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

        result = Check(tr_from=self.tr_from, tr_to=self.tr_to, amount=self.amount).check()

        if type(result) == str:
            return False, result

        if result[0]:
            self.tr_from.size -= self.amount
        else:
            self.tr_from.balance -= self.amount

        if result[1]:
            self.tr_to.size += self.amount
        else:
            self.tr_to.balance += self.amount

        self.tr_from.save()
        self.tr_to.save()
        return True, 'msg'


class Check(object):
    def __init__(self, num=None, validity=None, card_owner=None, cvc2_cvv=None, tr_from=None, tr_to=None, amount=None):
        self.num = num
        self.validity = validity
        self.card_owner = card_owner
        self.cvc2_cvv = cvc2_cvv
        self.tr_from = tr_from
        self.tr_to = tr_to
        self.amount = amount

    def check(self):
        if not self.tr_from and not self.tr_to and not self.amount:
            return 'error'
        result = list()
        for i in [self.tr_from, self.tr_to]:
            try:
                card = models.UserCard.objects.get(card_num=i.card_num)
                self.num = card.card_num
                self.validity = card.period_validity
                self.card_owner = card.name_card_owner
                self.cvc2_cvv = card.CVC2_CVV
                if not self.check_card():
                    return 'error'
                if card.size < self.amount:
                    return 'error'
                result.append(True)
            except:
                try:
                    balance = models.MyUser.objects.get(username=i.username)
                    if balance.balance < self.amount:
                        return 'error'
                    result.append(False)
                except:
                    return 'error'
        return result

    def check_card(self):
        try:
            models.UserCard.objects.get(card_num=self.num, period_validity=self.validity,
                                        name_card_owner=self.card_owner, CVC2_CVV=self.cvc2_cvv)
            return True
        except:
            return False
