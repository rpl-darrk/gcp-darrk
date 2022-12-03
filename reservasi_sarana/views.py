from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from .models import *
from pengguna.models import Pengguna
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def contohDaftar(request):
    return render(request, "contoh.html")


@login_required(login_url='/login/')
def verifikasiPembayaran(request, ID_sewa):
    if request.method == "POST":
        sewa_sarana, created = Sewa_Sarana.objects.get_or_create(
            ID_sewa=ID_sewa)
        sewa_sarana.ubahStatusPembayaran(Status_Detail_Pembayaran.VERIFIED)
        return HttpResponseRedirect('../contoh-daftar')


@login_required(login_url='/login/')
def pembatalanReservasi(request, ID_sewa):
    if request.method == "POST":
        sewa_sarana, created = Sewa_Sarana.objects.get_or_create(
            ID_sewa=ID_sewa)
        pengguna = Pengguna.objects.get(
            user=request.user)
        sewa_sarana.batalSewa(pengguna)
        return HttpResponseRedirect('../contoh-daftar')


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
        return HttpResponseRedirect('../contoh-daftar')
