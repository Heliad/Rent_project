from Bank_module import models
import json


class BankModule(object):
    def __init__(self, msg, way):
        self.myobj = json.loads(msg)

        self.period_validity = self.myobj['period_validity']
        self.card_num = self.myobj['card_num']
        self.name_card_owner = self.myobj['name_card_owner']
        self.CVC2_CVV = self.myobj['CVC2_CVV']
        self.size = self.myobj['size']
        self.way = way

    def check_card(self):
        complete = True
        msg = ''
        card = models.UserCard.objects.filter(card_num=self.card_num)
        card = card[0]
        if not card:
            complete = False
            msg = 'Введен номер несуществующей карты'
        else:
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
