from django import template


def mon_cost(arg, value):
    if not type(arg) == list:
        return float(arg) + float(arg) * value
    else:
        return 0


def percentage(arg):
    return str(arg * 100) + '%'


def card_num_beautify(arg):
    if type(arg) == str and not arg == 'Кошелек':
        return 'Карта ' + arg[:4] + ' XXXX XXXX ' + arg[-4:]
    else:
        return arg


register = template.Library()
register.filter('mon_cost', mon_cost)
register.filter('percentage', percentage)
register.filter('card_num_beautify', card_num_beautify)
