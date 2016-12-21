import datetime

from django.core.management.base import BaseCommand

from TOFI import models, transaction


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        auto_pay = models.AutoPayment.objects.all()
        self.stdout.write(str(datetime.datetime.today().strftime('%Y-%m-%d')))
        for pay in auto_pay:
            self.stdout.write(str(pay.next_payment_date))
            if str(pay.next_payment_date) == str(datetime.datetime.today().strftime('%Y-%m-%d')):
                payment = models.QuickPayment.objects.get(id=pay.quick_payment.id)
                if payment.user_payment == 'Кошелек':
                    tr_from = models.MyUser.objects.get(id=payment.username_id)
                else:
                    tr_from = models.UserCard.objects.get(card_num=payment.user_payment)
                tr_to = models.MyUser.objects.get(
                    id=models.Rent.objects.get(id=models.DoneRent.objects.get(id=payment.rent_id).id_house).user_login)
                c, m = transaction.Transaction(payment.amount, tr_from, tr_to).make_transaction()
                if c:
                    drent = models.DoneRent.objects.get(id=payment.rent_id)
                    drent.next_payment_date += datetime.timedelta(days=
                                                                  models.Rent.objects.get(id=
                                                                                          drent.id_house).payment_interval)
                    drent.save()
                    pay.next_payment_date += datetime.timedelta(days=pay.payment_interval)
                    pay.save()
                    # Логирование автоматического платежа платежа
                    user_id = models.QuickPayment.objects.get(id=pay.quick_payment_id).username_id
                    amount = models.QuickPayment.objects.get(id=pay.quick_payment_id).amount
                    models.LogOperationsBalance.objects.create(id_user=user_id,
                                                               type_operation='Выполнение автоматического платежа № ' +
                                                                              str(id),
                                                               describe_operation="Оплата на сумму " + str(
                                                                   payment.amount) + " BYN. " + str(m), status=c,
                                                               amount=amount, date_operation=datetime.date.today())
