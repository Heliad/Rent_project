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
from TOFI import views

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
    url(r'aboutUser/(?P<login_id>\d*)', views.aboutUser, name='AboutUser'),
    url(r'aboutHouse/(?P<number>\d*)', views.aboutHouse, name ='AboutHouse'),
    url(r'^admin/', admin.site.urls),
]
