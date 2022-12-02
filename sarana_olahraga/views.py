from django.shortcuts import render
from .models import GOR
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def getSaranaOlaharaga(request, ID_gor):
    if request.method == "GET":
        context = {}
        gor, created = GOR.objects.get_or_create(ID_gor=ID_gor)
        print(gor.nama)
        context = {"gor": gor, "daftar_sarana": gor.getSaranaGor()}
        return render(request, "sarana_olahraga.html", context)
