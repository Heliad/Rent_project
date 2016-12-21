from django.conf.urls import url, include

from TOFI import views, viewAdmin, viewModer
from user_profile import views as viewsProfile

urlpatterns = [
    url(r'^$', views.main_view, name='Main'),

    url(r'^register$', views.Registration.as_view(), name='Registration'),
    url(r'^login/', views.Login.as_view(), name='Login'),
    url(r'^logout/', views.logout_view, name='Logout'),

    url(r'^profile/', include('user_profile.urls')),

    url(r'^add_rent$', views.AddRent.as_view(), name='AddRent'),

    url(r'comment', views.comment, name='Comment'),

    url(r'search', include('search.urls')),

    url(r'aboutUser/(?P<login_id>\d*)', views.aboutUser, name='AboutUser'),
    url(r'make_complaint/(?P<id_user_to>\d*)', views.make_complaint, name='MakeComplaint'),

    url(r'makeRent/(?P<number>\d*)', views.make_rent, name='MakeRent'),
    url(r'aboutHouse/(?P<number>\d*)', views.aboutHouse, name='AboutHouse'),

    url(r'mainadmin', viewAdmin.main_admin, name='MainAdmin'),
    url(r'currency', viewAdmin.all_currency, name='AllCurrency'),
    url(r'editCurrency/(?P<id_cur>\d*)', viewAdmin.edit_currency, name='EditCurrency'),
    url(r'blockadmin', viewAdmin.blocked_accounts, name='BlockAccounts'),
    url(r'createblock/(?P<id_user>\d*)', viewAdmin.create_block, name='CreateBlock'),
    url(r'deleteblock/(?P<id_user>\d*)', viewAdmin.delete_block, name='DeleteBlock'),
    url(r'edituseradmin/(?P<id_user>\d*)', viewAdmin.edit_user_admin, name='EditUser'),
    url(r'monetization', viewAdmin.monetization, name='Monetization'),
    url(r'refill_balance_admin/(?P<id_user>\d*)', viewAdmin.refill_balance_admin, name='RefillBalanceAdmin'),

    url(r'main_moder', viewModer.main_moder, name='MainModer'),
    url(r'all_penalties', viewModer.all_penalties, name='AllPenalties'),
    url(r'add_penalty', viewModer.add_penalty, name='AddPenalty'),
    url(r'delete_penalty/(?P<id_penalty>\d*)', viewModer.delete_penalty, name='DeletePenalty'),
    url(r'edit_penalty/(?P<id_penalty>\d*)', viewModer.edit_penalty, name='EditPenalty'),
    url(r'all_complaints', viewModer.all_complaints, name='AllComplaints'),
    url(r'all_done_rents', viewModer.all_done_rents, name='AllDoneRents'),
    url(r'about_done_rent/(?P<id_done_rent>\d*)', viewModer.about_done_rent, name='AboutDoneRent'),

    url(r'delete_auto_payment/(?P<id>\d*)', viewsProfile.delete_auto_payment, name='DeleteAutoPayment'),
    url(r'edit_auto_payment/(?P<id>\d*)', viewsProfile.edit_auto_payment, name='EditAutoPayment'),
]
