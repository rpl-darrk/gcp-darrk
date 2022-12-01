from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from .models import Sewa_Sarana, Pembatalan_Sewa_Sarana, Verifikasi_Pembatalan


def contohDaftar(request):
    return render(request, "contoh.html")


def verifikasiPembayaran(request, ID_sewa):
    if request.method == "POST":
        sewa_sarana, created = Sewa_Sarana.objects.get_or_create(
            ID_sewa=ID_sewa)
        sewa_sarana.ubahStatusPembayaran("Pembayaran terverifikasi")
        return HttpResponseRedirect('../contoh-daftar')


def pembatalanReservasi(request, ID_sewa):
    if request.method == "POST":
        sewa_sarana, created = Sewa_Sarana.objects.get_or_create(
            ID_sewa=ID_sewa)
        sewa_sarana.batalSewa(request.user)
        return HttpResponseRedirect('../contoh-daftar')


def verifikasiPembatalan(request, ID_sewa):
    if request.method == "POST":
        sewa_sarana, created = Sewa_Sarana.objects.get_or_create(
            ID_sewa=ID_sewa)
        pembatalan, created = Pembatalan_Sewa_Sarana.objects.get_or_create(
            sewa_sarana=sewa_sarana)
        verifikasi_pembatalan, created = Verifikasi_Pembatalan.objects.get_or_create(
            pembatalan=pembatalan)
        verifikasi_pembatalan.verifikasiPembatalan()
        return HttpResponseRedirect('../contoh-daftar')
