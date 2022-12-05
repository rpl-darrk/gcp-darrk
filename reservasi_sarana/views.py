from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from .models import *
from pengguna.models import Pengguna, Konsumen_GOR
from django.contrib.auth.decorators import login_required
from pengguna.models import *
from .forms import UploadBuktiPembayaranForm
from datetime import datetime


@login_required(login_url='/login/')
def verifikasiPembayaran(request, ID_sewa):
    if request.method == "POST":
        sewa_sarana, created = Sewa_Sarana.objects.get_or_create(
            ID_sewa=ID_sewa)
        sewa_sarana.ubahStatusPembayaran(Status_Detail_Pembayaran.VERIFIED)
        return HttpResponseRedirect('../../daftar-reservasi')


@login_required(login_url='/login/')
def pembatalanReservasi(request, ID_sewa):
    if request.method == "POST":
        sewa_sarana, created = Sewa_Sarana.objects.get_or_create(
            ID_sewa=ID_sewa)
        pengguna = Pengguna.objects.get(
            user=request.user)
        sewa_sarana.batalSewa(pengguna)

        try:
            Pengurus_GOR.objects.get(user=request.user)
            return HttpResponseRedirect('../../daftar-reservasi')
        except Pengurus_GOR.DoesNotExist:
            return HttpResponseRedirect('../riwayat-reservasi')


@login_required(login_url='/login/')
def verifikasiPembatalan(request, ID_sewa):
    if request.method == "POST":
        sewa_sarana, created = Sewa_Sarana.objects.get_or_create(
            ID_sewa=ID_sewa)
        pembatalan, created = Pembatalan_Sewa_Sarana.objects.get_or_create(
            sewa_sarana=sewa_sarana)
        verifikasi_pembatalan, created = Verifikasi_Pembatalan.objects.get_or_create(
            pembatalan=pembatalan)

        sewa_sarana.updateStatus(Status_Sewa_Sarana.CANCELLED)
        verifikasi_pembatalan.verifikasiPembatalan()
        return HttpResponseRedirect('../../daftar-reservasi')


@login_required(login_url='/login/')
def cekRiwayatReservasi(request):

    context = {}

    if request.method == "GET":
        konsumen = Konsumen_GOR.objects.get(user=request.user)
        reservasi = Sewa_Sarana.objects.filter(konsumen=konsumen)

        list_reservasi = []
        for i in range(len(reservasi)):
            list_reservasi += [reservasi[i].ID_sewa]

        context = {
            'list_reservasi': list_reservasi
        }

        return render(request, 'riwayat_reservasi.html', context)


@login_required(login_url='/login/')
def get_daftar_reservasi(request):
    if request.method == "GET":
        pengurus_gor = Pengurus_GOR.objects.get(user=request.user)
        daftar_reservasi = Sewa_Sarana.objects.filter(pengurus=pengurus_gor)
        response = {'daftar_reservasi': daftar_reservasi}
        return render(request, 'daftar_reservasi.html', response)


@login_required(login_url='/login/')
def simpan_bukti_pembayaran(request):
    kg = Konsumen_GOR.objects.get(user=request.user)
    ss = Sewa_Sarana.objects.filter(konsumen=kg).get(
        status=Status_Sewa_Sarana.WAITTOPAY)
    dp = Detail_Pembayaran.objects.get(sewa_sarana=ss)
    form = UploadBuktiPembayaranForm(request.POST or None, instance=dp)
    if (form.is_valid() and request.method == 'POST'):
        f = form.save(commit=False)
        f.datetime = datetime.now()
        f.save()
        time_diff = dp.datetime - ss.datetime
        mins = time_diff.total_seconds()/60
        if mins <= 60:
            # lanjut
            dp.ubahStatusDetailPembayaran(Status_Detail_Pembayaran.WAITING)
            return HttpResponseRedirect('/')
        # batal
        ss.updateStatus(Status_Sewa_Sarana.CANCELLED)
        return HttpResponseRedirect('/')
    return render(request, 'form_upload_bukti_pembayaran.html', {'form': form})
