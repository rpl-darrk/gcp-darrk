from django.shortcuts import render, redirect
from django.views import defaults
from ..models import Jadwal_Reservasi, Sarana
from datetime import datetime, timezone
from django.http import HttpResponseRedirect


def reservasi(request, id_jadwal):
    if request.user.is_authenticated:
        if request.method == "POST":
            jadwal_reservasi = Jadwal_Reservasi.objects.get(
                ID_jadwal=id_jadwal)

            # if (jadwal_reservasi.status.__eq__(Status_Reservasi.VACANT)):
            #     jadwal_reservasi.status = Status_Reservasi.ORDERED
            #     jadwal_reservasi.save()
            #     return render(request, "reservasi_berhasil.html")
            # else:
            #     return render(request, "reservasi_gagal.html")
            return render(request, "reservasi_berhasil.html")
        else:
            return defaults.page_not_found(request, None)
    else:
        return redirect("login")


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
                        status = {'waktu': "{}|{}|{}".format(j - 1, jam_buka[i][0], jam_buka[i][1])}
                        if not hari_buka[j - 1]:
                            status['status'] = "Tutup"
                            status_book[i][j] = status
                        elif not status_book[i][j]:
                            status['status'] = "Tidak Tersedia"
                            status_book[i][j] = status
                        else:
                            status['status'] = "Tersedia"
                            status_book[i][j] = status

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
