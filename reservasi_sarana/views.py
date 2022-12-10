from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.views import defaults
from .models import *
from django.views.decorators.csrf import csrf_exempt
from sarana_olahraga.models import *
from django.contrib.auth.decorators import login_required
from pengguna.models import *
from .forms import UploadBuktiPembayaranForm
from sarana_olahraga.view.views_jadwal_reservasi import sinkronisasiDaftarTunggu
from datetime import datetime, timezone, timedelta


@login_required(login_url='/login/')
def reservasi(request, ID_gor, ID_sarana, waktu):
    konsumen = Konsumen_GOR.objects.get(user=request.user)
    if request.method == "POST":
        try:
            sarana = Sarana.objects.get(ID_sarana=ID_sarana)
            assert (sarana is not None)

            gor = sarana.gor
            jadwal = sarana.id_jadwal_reservasi
            assert (ID_gor == gor.ID_gor)

            time = waktu.split("|")
            hari = int(time[0])
            jam_mulai = time[1]
            jam_selesai = time[2]
            assert (0 <= hari and hari < 7)

            hari_buka = jadwal.hari_buka
            jam_buka = jadwal.jam_buka
            status_book = jadwal.status_book

            list_jam_buka = []

            for jam in jam_buka:
                list_jam_buka.append(jam[0] + "-" + jam[1])

            for i in range(len(status_book)):
                status_book[i].insert(0, list_jam_buka[i])
                for j in range(1, 8):
                    status = {'waktu': "{}|{}|{}".format(
                        j - 1, jam_buka[i][0], jam_buka[i][1])}
                    if not hari_buka[j - 1]:
                        status['status'] = "Tutup"
                        status_book[i][j] = status
                    elif not status_book[i][j]:
                        status['status'] = "Tidak Tersedia"
                        status_book[i][j] = status
                    else:
                        status['status'] = "Tersedia"
                        status_book[i][j] = status
            index = -1
            for i in range(len(jam_buka)):
                if (jam_buka[i][0] == jam_mulai and jam_buka[i][1] == jam_selesai):
                    index = i
                    break
            assert (index != -1)

            status_book = sinkronisasiDaftarTunggu(
                sarana.get_sewa_sarana().filter(status__exact=0),
                status_book
            )

            if hari_buka[hari] and status_book[index][hari+1]["status"] == "Tersedia":
                sewa_list = Sewa_Sarana.objects.all()
                id_max = 0
                for i in sewa_list:
                    if id_max<i.ID_sewa:
                        id_max = i.ID_sewa
                ID_Sewa = id_max + 1

                sewa_sarana = Sewa_Sarana.objects.create(
                    ID_sewa=ID_Sewa,
                    sarana=sarana,
                    konsumen=konsumen,
                    pengurus=gor.pengurus,
                    jam_booking=["%s-%s" % (jam_mulai, jam_selesai), hari]
                )
                sewa_sarana.save()

                detail_pembayaran = Detail_Pembayaran.objects.create(
                    sewa_sarana=sewa_sarana
                )
                detail_pembayaran.save()
                return HttpResponseRedirect("/info-pembayaran/%s" % sewa_sarana.ID_sewa)
            else:
                return HttpResponseRedirect("/jadwal/%s/%s" % (ID_gor, ID_sarana))
        except:
            return defaults.bad_request(request, None)
    else:
        return defaults.page_not_found(request, None)


@login_required(login_url='/login/')
def detail_pembayaran(request, ID_sewa):
    sewa_sarana = Sewa_Sarana.objects.get(ID_sewa=ID_sewa)
    detail_pembayaran = Detail_Pembayaran.objects.get(sewa_sarana=sewa_sarana)
    batas_waktu = sewa_sarana.datetime + timedelta(hours=1)
    pengurus_gor = sewa_sarana.pengurus
    sarana = sewa_sarana.sarana

    context = {
        "sarana": sarana,
        "batas_waktu": batas_waktu,
        "pengurus_gor": pengurus_gor,
        "sewa_sarana": sewa_sarana,
        "detail_pembayaran": detail_pembayaran,
    }
    return render(request, "info_pembayaran.html", context)

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