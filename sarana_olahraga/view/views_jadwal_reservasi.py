from django.shortcuts import render
from ..models import Sarana
from datetime import datetime, timezone
from django.http import HttpResponseRedirect


def get_jadwal_reservasi(request, id_gor, id_sarana):
    if request.method == 'GET':
        sarana = Sarana.objects.filter(ID_sarana=id_sarana).first()

        if sarana is not None:
            gor = sarana.gor

            if id_gor == gor.ID_gor:
                jadwal_reservasi = sarana.id_jadwal_reservasi

                hari_buka = jadwal_reservasi.hari_buka
                jam_buka = jadwal_reservasi.jam_buka
                status_book = jadwal_reservasi.status_book

                list_jam_buka = []

                for jam in jam_buka:
                    list_jam_buka.append(jam[0] + "-" + jam[1])

                for i in range(len(status_book)):
                    status_book[i].insert(0, list_jam_buka[i])
                    for j in range(1, 8):
                        if not hari_buka[j - 1]:
                            status_book[i][j] = "Tutup"
                        elif not status_book[i][j]:
                            status_book[i][j] = "Tidak Tersedia"
                        else:
                            status_book[i][j] = "Tersedia"

                daftar_tunggu = sarana.get_sewa_sarana().filter(status__exact=0)
                status_book = sinkronisasiDaftarTunggu(
                    daftar_tunggu, status_book)

                context = {
                    'sarana': sarana,
                    'status_book': status_book
                }

                return render(request, 'melihat_jadwal_reservasi/index.html', context)
    return HttpResponseRedirect('/mengelola_sarana_olahraga/')


def sinkronisasiDaftarTunggu(daftar_tunggu, status_book):
    for sewa_sarana in daftar_tunggu:
        jam_booking = sewa_sarana.jam_booking
        waktu_sewa = sewa_sarana.datetime
        difference = waktu_sewa.astimezone(
            timezone.utc) - datetime.now(timezone.utc)
        if difference.total_seconds() < -3600:
            sewa_sarana.status = 2
        else:
            for list_booking in status_book:
                if list_booking[0] == jam_booking[0]:
                    list_booking[jam_booking[1] + 1] = "Tidak Tersedia"

    return status_book
