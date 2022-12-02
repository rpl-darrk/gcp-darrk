from django.shortcuts import render

from mengelola_sarana_olahraga.models import GOR

def home(request):
    if request.user.is_authenticated:
        gor_list = GOR.objects.all()
        context = {
            "gor_list": gor_list,
        } 
        return render(request, "main/home.html", context)
    else:
        return render(request, "main/home.html")
