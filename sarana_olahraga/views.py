from django.shortcuts import render
from .models import GOR


def getSaranaOlaharaga(request, ID_gor):
    if request.method == "GET":
        context = {}
        gor, created = GOR.objects.get_or_create(ID_gor=ID_gor)
        context = {"daftar_sarana": gor.getSaranaGor()}
        return render(request, "sarana_olahraga.html", context)
