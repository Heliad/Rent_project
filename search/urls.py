from django.conf.urls import url

from TOFI import viewAdmin
from . import views

urlpatterns = [
    url(r'^$', views.search, name='Search'),
    url(r'search/searchrent', views.search_rent, name='SearchRent'),
    url(r'search/searchuser', views.search_user, name='SearchUser'),
    url(r'search/searchid', viewAdmin.search_by_id, name='SearchId'),
]
