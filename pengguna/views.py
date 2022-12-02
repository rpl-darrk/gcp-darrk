from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse

from .models import Pengguna, Konsumen_GOR, Pengurus_GOR

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:

            if Konsumen_GOR.objects.get(user=user) is not None:
                account = Konsumen_GOR.objects.get(user=user)
                msg = "{nama} berhasil login".format(nama=account.nama)
            else:
                account = Pengurus_GOR.objects.get(user=user)
                msg = "{nama} berhasil login".format(nama=account.nama)

            login(request, user)
            messages.success(request, msg)
                    
        else:
            messages.warning(request, "Username atau Password salah")
    
    context = {}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('login')