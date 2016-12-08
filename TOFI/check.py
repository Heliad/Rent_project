import datetime
from TOFI import models


# Проверка, выплачен ли штраф, если да - удалить
def check_payd_penalties():
    done_penalties = models.DonePenalty.objects.all()
    if done_penalties:
        for dp in done_penalties:
            if dp.is_payd:
                dp.delete()


def check_rent_number_pay():
    check_payd_penalties()

    all_done_rent = models.DoneRent.objects.all()

    # Обновление количества выплат, которые
    # пользователь уже должен был выплатить
    for r in all_done_rent:
        # Вычисление
        rent = models.Rent.objects.get(id=r.id_house)
        period_rent = rent.min_rent_time
        raw = datetime.date.today() - r.date_rent
        pay_number = raw.days // period_rent

        # Обновление
        r.pay_number = pay_number
        r.save()

        # Выдаем пиздюлей и письма
        penalty = models.Penalties.objects.get(id=1)
        check_repeat = models.DonePenalty.objects.filter(id_done_rent=r.id)  # Проверяем не высылали ли ему уже такое письмо
        if r.pay_number > r.paid_user:
            if not check_repeat:
                mes = "Вы просрочили платёж за аренду дома, под названием: " + rent.name + \
                      ", после прочтения этого письма, вам необходимо выплатить полную сумму штрафа," + \
                      " в размере: " + str(penalty.cost_penalty) + " BYN, а так же вам необходимо выплатить " + \
                      "полную сумму просрочки за аренду"
                models.DonePenalty.objects.create(describe_penalty=mes, id_user_for=r.id_user_renter,
                                                  size_penalty=penalty.cost_penalty, id_done_rent=r.id)
