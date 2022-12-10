from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from .models import Konsumen_GOR, Pengurus_GOR


@csrf_exempt
def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:

            try:
                Konsumen_GOR.objects.get(user=user)
                request.session['role'] = 'KONSUMEN'
            except:
                request.session['role'] = 'PENGURUS'

            login(request, user)
            return redirect('/')

        else:
            messages.warning(request, "Username atau Password salah")

    context = {}
    return render(request, 'login.html', context)


def userLogout(request):
    logout(request)
    request.session.pop("role", None)
    return redirect('/')
