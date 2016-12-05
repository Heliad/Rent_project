from django.shortcuts import render


def main_admin(request):
    return render(request, 'Admin/MainAdmin.html')