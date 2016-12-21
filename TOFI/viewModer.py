from django.http import HttpResponseRedirect
from django.shortcuts import render
from TOFI import models
from .forms import *


def main_moder(request):
    if request.user.is_anonymous or not request.user.is_moder:
        return HttpResponseRedirect("/login")

    return render(request, 'Moder/MainModer.html')


def all_penalties(request):
    if request.user.is_anonymous or not request.user.is_moder:
        return HttpResponseRedirect("/login")

    pen = models.Penalties.objects.all()
    return render(request, 'Moder/AllPenalties.html', {'pen': pen})


def add_penalty(request):
    if request.user.is_anonymous or not request.user.is_moder:
        return HttpResponseRedirect("/login")

    error = ''
    if request.method == 'POST':
        form = EditPenalty(request.POST)

        if form.is_valid():
            kind = form.cleaned_data['kind_penalty']
            describe = form.cleaned_data['describe_penalty']
            cost = form.cleaned_data['cost_penalty']

            models.Penalties.objects.create(kind_penalty=kind, describe_penalty=describe, cost_penalty=cost)
            mes = "Новый штраф успешно добавлен в систему!"
            return render(request, "Moder/Done.html", {'message': mes})

        else:
            err = form.errors.as_data()
            if 'kind_penalty' in err:
                error = 'Недопустимые символы в поле Название!'
            if 'describe_penalty' in err:
                error = 'Недопустимые символы в поле Описание!'
            if 'cost_penalty' in err:
                error = 'Недопустимые значение в поле Размер штрафа(Пример: XX,XXX)!'
    else:
        form = EditPenalty()

    return render(request, 'Moder/AddPenalty.html', {'form': form, 'error': error})


def delete_penalty(request, id_penalty):
    if request.user.is_anonymous or not request.user.is_moder:
        return HttpResponseRedirect("/login")

    pen = models.Penalties.objects.get(id=id_penalty)
    pen.delete()

    mes = "Штраф успешно удалён из системы!"
    return render(request, "Moder/Done.html", {'message': mes})


def edit_penalty(request, id_penalty):
    if request.user.is_anonymous or not request.user.is_moder:
        return HttpResponseRedirect("/login")

    error = ''
    pen = models.Penalties.objects.get(id=id_penalty)

    class EditPenalty(forms.Form):
        kind_penalty = forms.CharField(label="Название:", required=True, max_length=50, initial=pen.kind_penalty,
                                       validators=[RegexValidator('^[а-яёЁА-Я\ ]*$')])
        describe_penalty = forms.CharField(label="Описание:", required=True, max_length=150, widget=forms.Textarea,
                                           initial=pen.describe_penalty,
                                           validators=[RegexValidator('^[а-яЁёА-Я0-9\.\,\(\)\; ]*$')])
        cost_penalty = forms.FloatField(label="Размер штрафа:", required=True, initial=pen.cost_penalty,
                                        min_value=0, validators=[RegexValidator('^[0-9]{1,6}(,|.){1,1}[0-9]{1,2}$')]
                                        )

    if request.method == 'POST':
        form = EditPenalty(request.POST)

        if form.is_valid():
            kind = form.cleaned_data['kind_penalty']
            describe = form.cleaned_data['describe_penalty']
            cost = form.cleaned_data['cost_penalty']

            pen.kind_penalty = kind
            pen.describe_penalty = describe
            pen.cost_penalty = cost

            pen.save()
            mes = "Описание и сумма штрафа сохранены!"
            return render(request, "Moder/Done.html", {'message': mes})
        else:
            err = form.errors.as_data()
            if 'kind_penalty' in err:
                error = 'Недопустимые символы в поле Название!'
            if 'describe_penalty' in err:
                error = 'Недопустимые символы в поле Описание!'
            if 'cost_penalty' in err:
                error = 'Недопустимые значение в поле Размер штрафа(Пример: XX,XXX)!'

    else:
        form = EditPenalty()

    return render(request, "Moder/EditPenalty.html", {'form': form, 'error': error})


def all_complaints(request):
    if request.user.is_anonymous or not request.user.is_moder:
        return HttpResponseRedirect("/login")

    complaints = models.Complaint.objects.all()
    return render(request, 'Moder/AllComplaints.html', {'complaints': complaints})


def all_done_rents(request):
    if request.user.is_anonymous or not request.user.is_moder:
        return HttpResponseRedirect("/login")

    all_done_rents = models.DoneRent.objects.all()
    return render(request, 'Moder/AllDoneRents.html', {'all_done_rents': all_done_rents})


def about_done_rent(request, id_done_rent):
    if request.user.is_anonymous or not request.user.is_moder:
        return HttpResponseRedirect("/login")

    done_rent = models.DoneRent.objects.get(id=id_done_rent)
    name_house = models.Rent.objects.get(id=done_rent.id_house_id).name
    login_renter = models.MyUser.objects.get(id=done_rent.id_user_renter).username
    login_owner = models.MyUser.objects.get(id=done_rent.id_user_owner_id).username

    return render(request, 'Moder/AboutDoneRent.html', {'done_rent': done_rent, 'name_house': name_house,
                                                        'login_renter': login_renter, 'login_owner': login_owner,
                                                        'id_rent': done_rent.id_house_id})