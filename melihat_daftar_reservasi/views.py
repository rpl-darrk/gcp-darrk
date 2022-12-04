from datetime import datetime
from django.http import response
from django.http.response import Http404, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render
# from pengguna.models import Pengurus_GOR
# from reservasi_sarana.models import Sewa_Sarana
from testmodels.models import *
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

@login_required(login_url='/login/')
def get_daftar_reservasi(request):
    if request.method == "GET":
        pengurus_gor = Pengurus_GOR.objects.get(user = request.user)
        daftar_reservasi = Sewa_Sarana.objects.filter(pengurus = pengurus_gor)
        response = {'daftar_reservasi': daftar_reservasi}
        return render(request, 'daftar_reservasi.html', response)