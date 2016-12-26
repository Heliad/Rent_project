from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.profile, name='Profile'),
    url(r'changepassword', views.profileChangePassword, name='ChangePassword'),
    url(r'deletemyself', views.deleteMySelf, name='DeleteMySelf'),
    url(r'refillbalance', views.refillBalance, name='RefillBalance'),
    url(r'unfillbalance', views.unfillBalance, name='UnfillBalance'),
    url(r'add_card', views.add_card, name='AddCard'),
    url(r'delete_card/(?P<id>\d*)', views.delete_card, name='DeleteCard'),
    url(r'editprofile', views.edit_profile, name='EditProfile'),
    url(r'mails', views.mails, name='Mails'),
    url(r'acceptrent/(?P<id_mes>\d*)', views.accept_rent, name='AcceptRent'),
    url(r'rejectrent/(?P<id_mes>\d*)', views.reject_rent, name='RejectRent'),
    url(r'allrentsrenter', views.all_rents_renter, name='AllRentsRenter'),
    url(r'allrentsowner', views.all_rents_owner, name='AllRentsOwner'),
    url(r'choose_payment/(?P<id_donerent>\d*)', views.choose_payment, name='ChoosePayment'),
    url(r'extractbalance', views.extract_balance, name='ExtractBalance'),

    url(r'quickpayment', views.quick_payment, name='QuickPayment'),
    url(r'payment_info/(?P<id>\d*)', views.quick_payment_info, name='Info'),
    url(r'delete_quick_payment/(?P<id>\d*)', views.delete_quick_payment, name='DeleteQuickPayment'),
    url(r'edit_quick_payment/(?P<id>\d*)', views.edit_quick_payment, name='DeleteQuickPayment'),

    url(r'my_penalties', views.my_penalties, name='MyPenalties'),
    url(r'make_pay_penalties/(?P<id_penalty>\d*)', views.make_pay_penalty, name='MakePayPenalty'),

    url(r'my_houses_owner', views.my_all_houses_owner, name='MyAllHousesOwner'),
    url(r'edit_my_rent/(?P<id_rent>\d*)', views.edit_my_house, name='EditMyRent'),
    url(r'delete_my_rent/(?P<id_rent>\d*)', views.delete_my_house, name='DeleteMyRent'),

    url(r'owner_close_rent/(?P<rent_id>\d*)', views.owner_close_rent, name='OwnerCloseRent'),
    url(r'close_rent/(?P<rent_id>\d*)', views.close_rent, name='CloseRent'),


    url(r'add_auto_payment', views.add_auto_payment, name='AddAutoPayment'),
    url(r'about_auto_payment/(?P<id_auto>\d*)', views.about_auto_payment, name='AboutAutoPayment'),
    url(r'auto_payment', views.auto_payment, name='AutoPayment'),
]
