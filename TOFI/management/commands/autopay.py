import datetime
from TOFI import send_mail as sm

from django.core.management.base import BaseCommand

from TOFI import models, transaction


class Command(BaseCommand):
    def auto_pay(self):
        auto_pay = models.AutoPayment.objects.filter(next_payment_date=datetime.datetime.today().strftime('%Y-%m-%d'))
        self.stdout.write(str(datetime.datetime.today().strftime('%Y-%m-%d')))
        for pay in auto_pay:
            # Проверка на бан
            user_id = pay.username_id
            user = models.MyUser.objects.get(id=user_id)
            if user.is_active:
                #
                payment = models.QuickPayment.objects.get(id=pay.quick_payment.id)
                if payment.user_payment == 'Кошелек':
                    tr_from = models.MyUser.objects.get(id=payment.username_id)
                else:
                    tr_from = models.UserCard.objects.get(card_num=payment.user_payment)
                tr_to = models.MyUser.objects.get(
                    id=models.Rent.objects.get(
                        id=models.DoneRent.objects.get(id=payment.rent_id).id_house.id).user_login.id)
                c, m = transaction.Transaction(payment.amount, tr_from, tr_to).make_transaction()
                if c:
                    transaction.PaymentManager(payment.amount, models.DoneRent.objects.get(id=payment.rent_id)).run()
                    pay.next_payment_date += datetime.timedelta(days=pay.payment_interval)
                    pay.save()
                qp = models.QuickPayment.objects.get(id=pay.quick_payment_id)
                done_rent = models.DoneRent.objects.get(id=qp.rent_id)
                user_id = models.QuickPayment.objects.get(id=pay.quick_payment_id).username_id
                email_from = models.MyUser.objects.get(id=user_id).email
                amount = models.QuickPayment.objects.get(id=pay.quick_payment_id).amount
                models.LogOperationsBalance.objects.create(id_user=user_id,
                                                           type_operation='Выполнение автоматического платежа № ' +
                                                                          str(id),
                                                           describe_operation="Оплата на сумму " +
                                                                              str(payment.amount) + " BYN. " +
                                                                              str(m), status=c,
                                                           amount=amount, date_operation=datetime.date.today())
                sm.Sender("Оплата аренды с помощью автоматического платежа",
                          "Оплата аренды №" + str(done_rent.id_house_id) + " на сумму " +
                          str(amount) + " BYN. " + str(m), email_from).sender()

                qp = models.QuickPayment.objects.get(id=pay.quick_payment_id)
                done_rent = models.DoneRent.objects.get(id=qp.rent_id)
                email_to = models.MyUser.objects.get(id=done_rent.id_user_owner_id)
                amount = models.QuickPayment.objects.get(id=pay.quick_payment_id).amount
                models.LogOperationsBalance.objects.create(id_user=done_rent.id_user_owner_id,
                                                           type_operation='Оплата автоматическим платежом № ' +
                                                                          str(id),
                                                           describe_operation="Оплата аренды на сумму " + str(
                                                               payment.amount) + " BYN. " + str(m), status=c,
                                                           amount=amount, date_operation=datetime.date.today())
                sm.Sender("Оплата аренды с помощью автоматического платежа",
                          "Оплата аренды №" + str(done_rent.id_house_id) + " на сумму " +
                          str(amount) + " BYN. " + str(m), email_to).sender()

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
