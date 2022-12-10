from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from .models import *
from django.contrib.auth.decorators import login_required
from pengguna.models import *
from .forms import UploadBuktiPembayaranForm
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from sarana_olahraga.models import *


@csrf_exempt
@login_required(login_url='/login/')
def verifikasiPembayaran(request):
    if request.method == "POST":
        ID_sewa = request.POST.get('ID_sewa', None)
        sewa_sarana, created = Sewa_Sarana.objects.get_or_create(
            ID_sewa=ID_sewa)
        sewa_sarana.ubahStatusPembayaran(Status_Detail_Pembayaran.VERIFIED)
        return HttpResponseRedirect('../../daftar-reservasi')


@csrf_exempt
@login_required(login_url='/login/')
def pembatalanReservasi(request):
    if request.method == "POST":
        ID_sewa = request.POST.get('ID_sewa', None)
        sewa_sarana, created = Sewa_Sarana.objects.get_or_create(
            ID_sewa=ID_sewa)
        pengguna = Pengguna.objects.get(
            user=request.user)
        sewa_sarana.batalSewa(pengguna)

        sinkronisasiPembatalan(sewa_sarana)

        try:
            Pengurus_GOR.objects.get(user=request.user)
            return HttpResponseRedirect('../../daftar-reservasi')
        except Pengurus_GOR.DoesNotExist:
            return HttpResponseRedirect('../riwayat-reservasi')


def sinkronisasiPembatalan(sewa_sarana):
    jadwal_booking = sewa_sarana.jam_booking
    sarana = sewa_sarana.sarana
    jadwal_reservasi = sarana.id_jadwal_reservasi

    waktu = jadwal_booking[0]
    hari = jadwal_booking[1]

    waktu_awal = waktu.split('-')[0]

    for i in jadwal_reservasi.jam_buka:
        if i[0] == waktu_awal:
            jadwal_reservasi.status_book[hari] = True
            jadwal_reservasi.save()
            break


@csrf_exempt
@login_required(login_url='/login/')
def verifikasiPembatalan(request):
    if request.method == "POST":
        ID_sewa = request.POST.get('ID_sewa', None)
        sewa_sarana, created = Sewa_Sarana.objects.get_or_create(
            ID_sewa=ID_sewa)
        pembatalan, created = Pembatalan_Sewa_Sarana.objects.get_or_create(
            sewa_sarana=sewa_sarana)
        verifikasi_pembatalan, created = Verifikasi_Pembatalan.objects.get_or_create(
            pembatalan=pembatalan)

        sewa_sarana.updateStatus(Status_Sewa_Sarana.CANCELLED)
        verifikasi_pembatalan.verifikasiPembatalan()
        return HttpResponseRedirect('../../daftar-reservasi')


@csrf_exempt
def selesaikanReservasi(request):
    if request.method == "POST":
        ID_sewa = request.POST.get('ID_sewa', None)
        sewa_sarana, created = Sewa_Sarana.objects.get_or_create(
            ID_sewa=ID_sewa)
        sewa_sarana.updateStatus(Status_Sewa_Sarana.DONE)
        return HttpResponseRedirect('../../daftar-reservasi')


@login_required(login_url='/login/')
def cekRiwayatReservasi(request):

    if request.method == "GET":
        konsumen_gor = Konsumen_GOR.objects.get(user=request.user)
        ss = Sewa_Sarana.objects.filter(konsumen=konsumen_gor)
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
            dict_r['gor'] = ss[i].sarana.gor.nama
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
        response = {'konsumen_gor': konsumen_gor,
                    'dr_menunggu_verif_bayar': dr_menunggu_verif_bayar,
                    'dr_menunggu_verif_batal': dr_menunggu_verif_batal,
                    'dr_menunggu_pembayaran': dr_menunggu_pembayaran,
                    'dr_berlangsung': dr_berlangsung,
                    'dr_selesai': dr_selesai,
                    'dr_batal': dr_batal}
        return render(request, 'riwayat_reservasi.html', response)

def get_hari(i):
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    return hari[i]


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
