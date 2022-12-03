from django.shortcuts import render
from jadwal_reservasi.models import Jadwal_Reservasi, Status_Reservasi

def reservasi(request, id_jadwal):
    jadwal_reservasi = Jadwal_Reservasi.objects.get(id_jadwal=id_jadwal)

    if (jadwal_reservasi.status.__eq__(Status_Reservasi.VACANT)):
        jadwal_reservasi.status = Status_Reservasi.ORDERED
        jadwal_reservasi.save()
        return render(request, "reservasi_berhasil.html")
    else:
        return render(request, "reservasi_gagal.html")
