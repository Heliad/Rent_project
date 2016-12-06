"""TOFI_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from TOFI import views, viewAdmin

urlpatterns = [
    url(r'^$', views.main_view, name='Main'),
    url(r'^login/', views.Login.as_view(), name='Login'),
    url(r'^logout/', views.logout_view, name='Logout'),
    url(r'^add_rent$', views.AddRent.as_view(), name='AddRent'),
    url(r'^register$', views.Registration.as_view(), name='Registration'),
    url(r'^profile$', views.profile, name='Profile'),
    url(r'changepassword', views.profileChangePassword, name='ChangePassword'),
    url(r'deletemyself', views.deleteMySelf, name='DeleteMySelf'),
    url(r'refillbalance', views.refillBalance, name='RefillBalance'),
    url(r'unfillbalance', views.unfillBalance, name='UnfillBalance'),
    url(r'add_card', views.add_card, name='AddCard'),
    url(r'editprofile', views.edit_profile, name='EditProfile'),
    url(r'mails', views.mails, name='Mails'),
    url(r'acceptrent/(?P<id_mes>\d*)', views.accept_rent, name='AcceptRent'),
    url(r'rejectrent/(?P<id_mes>\d*)', views.reject_rent, name='RejectRent'),
    url(r'allrentsrenter', views.all_rents_renter, name='AllRentsRenter'),
    url(r'allrentsowner', views.all_rents_owner, name='AllRentsOwner'),
    url(r'choose_payment/(?P<id_donerent>\d*)', views.choose_payment, name='ChoosePayment'),
    url(r'extractbalance', views.extract_balance, name='ExtractBalance'),
    url(r'quickpayment', views.quick_payment, name='QuickPayment'),
    url(r'addcommentuser/(?P<user_id>\d*)', views.add_comment_about_user, name='AddCommentAboutUser'),
    url(r'allcommentsuser/(?P<user_id>\d*)', views.all_comments_about_user, name='AllCommentsUser'),
    url(r'addcomment', views.add_comment, name='AddComment'),
    url(r'allcomments', views.all_comments, name='AllComments'),
    url(r'search/searchrent', views.search_rent, name='SearchRent'),
    url(r'search/searchuser', views.search_user, name='SearchUser'),
    url(r'search/searchid', viewAdmin.search_by_id, name='SearchId'),
    url(r'search', views.search, name='Search'),
    url(r'payment_info/(?P<id>\d*)', views.quick_payment_info, name='Info'),
    url(r'aboutUser/(?P<login_id>\d*)', views.aboutUser, name='AboutUser'),
    url(r'makeRent/(?P<number>\d*)', views.make_rent, name ='MakeRent'),
    url(r'aboutHouse/(?P<number>\d*)', views.aboutHouse, name ='AboutHouse'),

    url(r'^admin/', admin.site.urls),
    url(r'mainadmin', viewAdmin.main_admin, name='MainAdmin'),
    url(r'currency', viewAdmin.all_currency, name='AllCurrency'),
    url(r'editCurrency/(?P<id_cur>\d*)', viewAdmin.edit_currency, name='EditCurrency'),
    url(r'blockadmin', viewAdmin.blocked_accounts, name='BlockAccounts'),
    url(r'createblock/(?P<id_user>\d*)', viewAdmin.create_block, name='CreateBlock'),
    url(r'deleteblock/(?P<id_user>\d*)', viewAdmin.delete_block, name='DeleteBlock'),
    url(r'edituseradmin/(?P<id_user>\d*)', viewAdmin.edit_user_admin, name='EditUser'),
]
