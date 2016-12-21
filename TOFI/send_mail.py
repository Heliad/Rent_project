from django.core.mail import send_mail


class Sender(object):
    def __init__(self, subject, message, email_to):
        self.subject = subject
        self.message = message
        self.email_from = "nandsrenter@mail.ru"
        self.password_from = "1234567890qwertY"
        self.email_to = email_to

    def sender(self):
        try:
            send_mail(self.subject, self.message, 'NandSRenter@mail.ru', [self.email_to], fail_silently=True)
        except:
            pass