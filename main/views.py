from django.shortcuts import render, redirect

from sarana_olahraga.models import GOR


def home(request):
    return render(request, "main/home.html")

def gor_list(request):
    if request.user.is_authenticated:
        gor_list = GOR.objects.all()
        context = {
            "gor_list": gor_list,
        }
        return render(request, "main/gor_list.html", context)
    else:
        return redirect("login")