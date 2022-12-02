from django.shortcuts import render
from jadwal_reservasi.models import Jadwal_Reservasi, Status_Reservasi

def reservasi(request, id):
    jadwal_reservasi = Jadwal_Reservasi.objects.get(id=id)

    if (jadwal_reservasi.status == Status_Reservasi.VACANT):
        jadwal_reservasi.status = Status_Reservasi.ORDERED
        return render(request, "reservasi_berhasil.html")
    else:
        return render(request, "reservasi_gagal.html")
