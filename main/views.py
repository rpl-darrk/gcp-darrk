from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from sarana_olahraga.models import GOR


def home(request):
    return render(request, "main/home.html")

@login_required(login_url='/login/')
def gor_list(request):
    gor_list = GOR.objects.all()
    context = {
        "gor_list": gor_list,
    }
    return render(request, "main/gor_list.html", context)