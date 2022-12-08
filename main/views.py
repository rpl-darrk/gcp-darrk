from django.shortcuts import render, redirect

from sarana_olahraga.models import GOR


def home(request):
    return render(request, "main/home.html")
