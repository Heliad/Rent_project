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
        card = card[0]
        if self.way == 'in':
            if card.size >= self.size:
                complete = True
                self.update_card(card, self.way)
            else:
                complete = False
                msg = 'На карте не хватает средств'
        elif self.way == 'out':
            complete = True
            self.update_card(card, self.way)
        elif self.way == 'chsk':
            complete = True

        return complete, msg

    def update_card(self, card, way):
        if way == 'in':
            card.size -= self.size
        elif way == 'out':
            card.size += self.size
        card.save()
