from django import template


def mon_cost(arg, value):
    if not type(arg) == list:
        result = float(arg) + float(arg) * value
        if int(result) == result:
            return int(result)
        else:
            return round(float(result), 2)
    else:
        return 0


def percentage(arg):
    result = arg * 100
    if int(result) == result:
        return str(int(result)) + '%'
    else:
        return str(round(float(arg), 2)) + '%'


def card_num_beautify(arg):
    if type(arg) == str and not arg == 'Кошелек':
        return 'Карта ' + arg[:4] + ' XXXX XXXX ' + arg[-4:]
    else:
        return arg


def round_f(arg):
    if type(arg) == float:
        return round(float(arg), 2)
    else:
        try:
            return int(arg)
        except:
            return arg


register = template.Library()
register.filter('mon_cost', mon_cost)
register.filter('percentage', percentage)
register.filter('card_num_beautify', card_num_beautify)
register.filter('round_f', round_f)
