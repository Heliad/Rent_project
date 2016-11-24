import json
import urllib
from Bank_module import transaction as t


class Transaction(object):
    def __init__(self, card_num, period_validity, name_card_owner, CVC2_CVV, size):
        self.card_num = card_num
        self.period_validity = period_validity
        self.name_card_owner = name_card_owner
        self.CVC2_CVV = CVC2_CVV
        self.size = size

    def send(self, way):
        msg = json.dumps({'card_num': self.card_num, 'period_validity': self.period_validity,
                          'name_card_owner': self.name_card_owner, 'CVC2_CVV': self.CVC2_CVV, 'size': self.size})
        tr = t.BankModule(msg, way)

        is_complete, msg = tr.check_card()
        return is_complete, msg


