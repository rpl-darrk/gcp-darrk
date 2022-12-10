from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from sarana_olahraga.models import GOR


def home(request):
    return render(request, "main/home.html")
