import datetime

from django.core.management.base import BaseCommand

from TOFI import models, transaction


class Command(BaseCommand):
    def auto_pay(self):
        auto_pay = models.AutoPayment.objects.filter(next_payment_date=datetime.datetime.today().strftime('%Y-%m-%d'))
        self.stdout.write(str(datetime.datetime.today().strftime('%Y-%m-%d')))
        for pay in auto_pay:
            payment = models.QuickPayment.objects.get(id=pay.quick_payment.id)
            if payment.user_payment == 'Кошелек':
                tr_from = models.MyUser.objects.get(id=payment.username_id)
            else:
                tr_from = models.UserCard.objects.get(card_num=payment.user_payment)
            tr_to = models.MyUser.objects.get(
                id=models.Rent.objects.get(id=models.DoneRent.objects.get(id=payment.rent_id).id_house).user_login)
            c, m = transaction.Transaction(payment.amount, tr_from, tr_to).make_transaction()
            if c:
                transaction.PaymentManager(payment.amount, models.DoneRent.objects.get(id=payment.rent_id)).run()
                pay.next_payment_date += datetime.timedelta(days=pay.payment_interval)
                pay.save()
            user_id = models.QuickPayment.objects.get(id=pay.quick_payment_id).username_id
            amount = models.QuickPayment.objects.get(id=pay.quick_payment_id).amount
            models.LogOperationsBalance.objects.create(id_user=user_id,
                                                       type_operation='Выполнение автоматического платежа № ' +
                                                                      str(id),
                                                       describe_operation="Оплата на сумму " + str(
                                                           payment.amount) + " BYN. " + str(m), status=c,
                                                       amount=amount, date_operation=datetime.date.today())

    def fine_check(self):
        rent = models.DoneRent.objects.filter(next_payment_date=(datetime.datetime.today()
                                                                 - datetime.timedelta(days=1)))
        for r in rent:
            r.fine += (float(r.cost) - float(r.payed_until_time)) * 0.05
            self.stdout.write(str(r.next_payment_date))
            self.stdout.write(str(r.fine))
            r.save()

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.auto_pay()
        self.fine_check()
