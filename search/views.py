from django.shortcuts import render

from TOFI import models
from TOFI.forms import *


def search(request):
    return render(request, "Search/Search.html")


def search_rent(request):
    if request.method == 'POST':
        form = SearchRent(request.POST)

        if form.is_valid():
            results = []
            type_search = form.cleaned_data['type_search']
            max_interval = form.cleaned_data['max_interval']
            min_interval = form.cleaned_data['min_interval']
            login_or_name_rent = form.cleaned_data['login_or_name_rent']
            square = form.cleaned_data['square']
            if type_search == '1':
                temp = list(models.Rent.objects.all())
                for rent in temp:
                    if int(rent.cost) <= max_interval:
                        if int(rent.cost) >= min_interval:
                            results.append(rent)
            if type_search == '2':
                results = list(models.Rent.objects.all().filter(name=login_or_name_rent))
            if type_search == '3':
                user_id_login = models.MyUser.objects.get(username=login_or_name_rent)
                results = list(models.Rent.objects.all().filter(user_login=user_id_login.id))
            if type_search == '4':
                temp = list(models.Rent.objects.all())
                for rent in temp:
                    if int(rent.area) <= square:
                        results.append(rent)

            return render(request, 'Search/SearchRent.html', {'form': form, 'results': results})
    else:
        form = SearchRent()
        return render(request, "Search/SearchRent.html", {'form': form})


def search_user(request):
    if request.method == 'POST':
        form = SearchUser(request.POST)

        if form.is_valid():
            results = None
            type_search = form.cleaned_data['type_search']
            attr_search = form.cleaned_data['field_search']
            if type_search == '1':
                results = models.MyUser.objects.all().filter(username=attr_search)
            if type_search == '2':
                results = models.MyUser.objects.all().filter(surname=attr_search)
            if type_search == '3':
                results = models.MyUser.objects.all().filter(email=attr_search)
            return render(request, 'Search/SearchUser.html', {'form': form, 'results': results})
    else:
        form = SearchUser()
        return render(request, "Search/SearchUser.html", {'form': form})
