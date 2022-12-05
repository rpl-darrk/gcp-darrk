from datetime import datetime
from django.http import response
from django.http.response import Http404, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from pengguna.models import Konsumen_GOR
from reservasi_sarana.models import Detail_Pembayaran, Sewa_Sarana
from .forms import UploadBuktiPembayaranForm
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

@login_required(login_url='/login/')
def simpan_bukti_pembayaran(request):
    kg = Konsumen_GOR.objects.get(user = request.user)
    ss = Sewa_Sarana.objects.filter(konsumen = kg).get(status = Status_Sewa_Sarana.WAITTOPAY)
    dp = Detail_Pembayaran.objects.get(sewa_sarana = ss)
    form = UploadBuktiPembayaranForm(request.POST or None, instance = dp)
    if (form.is_valid() and request.method == 'POST'):
        f = form.save(commit = False)
        f.datetime = datetime.now()
        f.save()
        time_diff = dp.datetime - ss.datetime
        mins = time_diff.total_seconds()/60
        if mins <= 60:
            # lanjut
            dp.ubahDetailPembayaran(Status_Detail_Pembayaran.WAITING)
            return HttpResponseRedirect('/')
        # batal
        ss.updateStatus(Status_Sewa_Sarana.CANCELLED)
        return HttpResponseRedirect('/')
    return render(request, 'form_upload_bukti_pembayaran.html', {'form': form})
