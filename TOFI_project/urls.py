from django.conf.urls import url, include

from TOFI import views, viewAdmin

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
    url(r'makeRent/(?P<number>\d*)', views.make_rent, name='MakeRent'),
    url(r'aboutHouse/(?P<number>\d*)', views.aboutHouse, name='AboutHouse'),

    url(r'mainadmin', viewAdmin.main_admin, name='MainAdmin'),
    url(r'currency', viewAdmin.all_currency, name='AllCurrency'),
    url(r'editCurrency/(?P<id_cur>\d*)', viewAdmin.edit_currency, name='EditCurrency'),
    url(r'blockadmin', viewAdmin.blocked_accounts, name='BlockAccounts'),
    url(r'createblock/(?P<id_user>\d*)', viewAdmin.create_block, name='CreateBlock'),
    url(r'deleteblock/(?P<id_user>\d*)', viewAdmin.delete_block, name='DeleteBlock'),
    url(r'edituseradmin/(?P<id_user>\d*)', viewAdmin.edit_user_admin, name='EditUser'),
]
