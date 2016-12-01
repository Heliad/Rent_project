from TOFI import models


class BankModule(object):
    def __init__(self, card_num, period_validity, name_card_owner, CVC2_CVV, way, size=0):

        self.period_validity = period_validity
        self.card_num = card_num
        self.name_card_owner = name_card_owner
        self.CVC2_CVV = CVC2_CVV
        self.size = size
        self.way = way

    def check_card(self):
        complete = True
        msg = ''
        card = models.UserCard.objects.filter(card_num=self.card_num, period_validity=self.period_validity,
                                              name_card_owner=self.name_card_owner, CVC2_CVV=self.CVC2_CVV)
        if not card:
            return False, 'Введены неверные данные'
        self.card = card[0]
        if self.way == 'in':
            if card.size >= self.size:
                complete = True
                self.update_card()
            else:
                complete = False
                msg = 'На карте не хватает средств'
        elif self.way == 'out':
            complete = True
            self.update_card()
        elif self.way == 'chsk':
            complete = True
        elif self.way == 'pay':
            return self.pay()

        return complete, msg

    def update_card(self):
        if self.way == 'in':
            self.card.size -= self.size
        elif self.way == 'out':
            self.card.size += self.size
        self.card.save()

    def pay(self, card_to):
        self.way = 'in'
        self.update_card()
        self.way = 'out'
        self.card = card_to
        self.update_card()
