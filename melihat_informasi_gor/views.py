from datetime import datetime
from django.http import response
from django.http.response import Http404, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render
# from pengguna.models import Pengurus_GOR
# from sarana_olahraga.models import GOR
from testmodels.models import *
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

@login_required(login_url='/login/')
def get_info_gor(request, ID_gor):
    if request.method == "GET":
        gor = GOR.objects.get(ID_gor = ID_gor)
        response = {'nama': gor.nama,
                    'url_foto': gor.url_foto,
                    'alamat': gor.alamat,
                    'no_telepon': gor.no_telepon}
        return render(request, 'info_gor.html', response)