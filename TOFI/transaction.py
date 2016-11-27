from TOFI import models


class BankModule(object):
    def __init__(self, card_num, period_validity, name_card_owner, CVC2_CVV, size, way):

        self.period_validity = period_validity
        self.card_num = card_num
        self.name_card_owner = name_card_owner
        self.CVC2_CVV = CVC2_CVV
        self.size = size
        self.way = way

    def check_card(self):
        complete = True
        msg = ''
        card = models.UserCard.objects.filter(card_num=self.card_num)
        if not card:
            complete = False
            msg = 'Введен номер несуществующей карты'
        else:
            card = card[0]
            if card.period_validity == self.period_validity \
                    and card.name_card_owner == self.name_card_owner and card.CVC2_CVV == self.CVC2_CVV:
                if self.way == 'in':
                    if card.size >= self.size:
                        complete = True
                        self.update_card(card, self.way)
                    else:
                        complete = False
                        msg = 'На карте не хватает средств'
                else:
                    complete = True
                    self.update_card(card, self.way)
            else:
                complete = False
                msg = 'Введены неверные данные'

        return complete, msg

    def update_card(self, card, way):
        if way == 'in':
            card.size = card.size - self.size
        else:
            card.size = card.size + self.size
        card.save()
