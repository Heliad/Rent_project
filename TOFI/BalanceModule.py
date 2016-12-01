from TOFI import models


class BalanceModule():
    def __init__(self, id_user, sum):
        self.user = models.MyUser.objects.get(id=id_user)
        self.sum = sum

    def check_balance(self):
        if self.user.balance < self.sum:
            return False
        else:
            return True

    def pay(self, id_user_to):
        if self.check_balance():
            self.user.balance -= self.sum
            self.user.save()
            user_to = models.MyUser.objects.get(id=id_user_to)
            user_to.balance += self.sum
            user_to.save()
