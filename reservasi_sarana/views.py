from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from .models import *
from pengguna.models import Pengguna, Konsumen_GOR
from django.contrib.auth.decorators import login_required
from pengguna.models import *
from .forms import UploadBuktiPembayaranForm
from datetime import datetime, timezone, timedelta
from sarana_olahraga.models import *


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
        gor = GOR.objects.get(pengurus = pengurus_gor)
        ss = Sewa_Sarana.objects.filter(pengurus=pengurus_gor)
        dr_menunggu_verif_bayar = []
        dr_menunggu_verif_batal = []
        dr_menunggu_pembayaran = []
        dr_berlangsung = []
        dr_selesai = []
        dr_batal = []
        dict_r = dict()
        for i in range(ss.count()):
            dict_r['ss'] = ss[i]
            dict_r['dp'] = Detail_Pembayaran.objects.get(sewa_sarana = ss[i])
            dict_r['hari'] = get_hari(ss[i].jam_booking[1])
            dict_r['pesan'] = ss[i].datetime + timedelta(hours=7)
            if ss[i].status == '2':
                dr_batal.append(dict_r.copy())
            elif ss[i].status == '3':
                dr_selesai.append(dict_r.copy())
            elif ss[i].status == '1':
                if Pembatalan_Sewa_Sarana.objects.filter(sewa_sarana = ss[i]).first() != None:
                    dr_menunggu_verif_batal.append(dict_r.copy())
                else:
                    dr_berlangsung.append(dict_r.copy())
            elif ss[i].status == '0':
                if Detail_Pembayaran.objects.get(sewa_sarana = ss[i]).status == '0':
                    dr_menunggu_pembayaran.append(dict_r.copy())
                elif Detail_Pembayaran.objects.get(sewa_sarana = ss[i]).status == '1':
                    dr_menunggu_verif_bayar.append(dict_r.copy())
        response = {'gor': gor,
                    'dr_menunggu_verif_bayar': dr_menunggu_verif_bayar,
                    'dr_menunggu_verif_batal': dr_menunggu_verif_batal,
                    'dr_menunggu_pembayaran': dr_menunggu_pembayaran,
                    'dr_berlangsung': dr_berlangsung,
                    'dr_selesai': dr_selesai,
                    'dr_batal': dr_batal}
        return render(request, 'daftar_reservasi.html', response)

def get_hari(i):
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    return hari[i]

@login_required(login_url='/login/')
def simpan_bukti_pembayaran(request, ID_sewa):
    ss = Sewa_Sarana.objects.get(ID_sewa = ID_sewa)
    if ss.konsumen.user != request.user:
        return HttpResponseForbidden("You are not allowed to access this page because the ID is not yours.")
    dp = Detail_Pembayaran.objects.get(sewa_sarana = ss)
    if ss.status != '0' or dp.status != '0':
        return HttpResponseForbidden("The reservation is already paid, cancelled, or waiting for verification.")
    form = UploadBuktiPembayaranForm(request.POST or None, instance = dp)
    if (form.is_valid() and request.method == 'POST'):
        f = form.save(commit=False)
        f.datetime = datetime.now(timezone.utc)
        f.save()
        time_diff = dp.datetime - ss.datetime
        mins = time_diff.total_seconds()/60
        if mins <= 60:
            # lanjut
            dp.ubahStatusDetailPembayaran('1')
            return HttpResponseRedirect('/riwayat-reservasi')
        # batal
        ss.updateStatus('2')
        return HttpResponseForbidden("Mohon maaf, batas waktu pembayaran Anda sudah terlewat. Silakan menghubungi GOR yang bersangkutan untuk ditangani lebih lanjut.")
    return render(request, 'form_upload_bukti_pembayaran.html', {'form': form, 'jam': ss.jam_booking[0], 'hari': get_hari(ss.jam_booking[1])})