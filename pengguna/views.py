from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Konsumen_GOR, Pengurus_GOR


def userLogin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:

            try:
                account = Konsumen_GOR.objects.get(user=user)
                msg = "{nama} berhasil login".format(nama=account.nama)
            except:
                account = Pengurus_GOR.objects.get(user=user)
                msg = "{nama} berhasil login".format(nama=account.nama)

            login(request, user)
            messages.success(request, msg)

        else:
            messages.warning(request, "Username atau Password salah")

    context = {}
    return render(request, 'login.html', context)


def userLogout(request):
    logout(request)
    return redirect('login')
