from django.http import HttpResponseRedirect
from django.shortcuts import render
from TOFI import models
from .forms import *


def main_moder(request):
    return render(request, 'Moder/MainModer.html')


def all_penalties(request):
    pen = models.Penalties.objects.all()
    return render(request, 'Moder/AllPenalties.html', {'pen': pen})


def add_penalty(request):
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
        form = EditPenalty()

    return render(request, 'Moder/AddPenalty.html', {'form': form})


def delete_penalty(request, id_penalty):
    pen = models.Penalties.objects.get(id=id_penalty)
    pen.delete()

    mes = "Штраф успешно удалён из системы!"
    return render(request, "Moder/Done.html", {'message': mes})


def edit_penalty(request, id_penalty):
    pen = models.Penalties.objects.get(id=id_penalty)

    class EditPenalty(forms.Form):
        kind_penalty = forms.CharField(label="Название:", required=True, max_length=50, initial=pen.kind_penalty)
        describe_penalty = forms.CharField(label="Описание:", required=True, max_length=150, initial=pen.describe_penalty, widget=forms.Textarea)
        cost_penalty = forms.FloatField(label="Размер штрафа:", required=True, initial=pen.cost_penalty)

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
        form = EditPenalty()

    return render(request, "Moder/EditPenalty.html", {'form': form})

