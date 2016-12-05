from django.http import HttpResponseRedirect
from django.shortcuts import render
from TOFI import models
from .forms import *

def main_admin(request):
    return render(request, 'Admin/MainAdmin.html')


def blocked_accounts(request):
    blocked_accounts = models.MyUser.objects.all()
    return render(request, 'Admin/BlockedAccounts.html', {'blocked_accounts': blocked_accounts})


def create_block(request, id_user):
    if request.method == 'POST':
        form = CreateBlock(request.POST)

        if form.is_valid():
            reason = form.cleaned_data['reason_block']
            user = models.MyUser.objects.get(id=id_user)
            user.reason_block = reason
            user.is_active = 0
            user.save()
            mes = user.username + " заблокирован"
            return render(request, 'Admin/Done.html', {'message': mes})
    else:
        form = CreateBlock()

    #return render(request, 'Profile/RefillBalance.html', {'form': form}
    return render(request, 'Admin/CreateBlock.html', {'form': form})

