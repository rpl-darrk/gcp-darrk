from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pengguna.models import Konsumen_GOR

from .models import Sewa_Sarana

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