from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from json import JSONEncoder
from django.contrib.auth.decorators import login_required

import json

from ..models import GOR, Jadwal_Reservasi, Sarana
from pengguna.models import Pengurus_GOR


def initTabelJadwal():

    hari_buka = []
    jam_buka = [[]]
    status_book = [[False for i in range(len(hari_buka))]
                   for i in range(len(jam_buka))]

    new_jadwal = Jadwal_Reservasi(
        hari_buka=JSONEncoder().encode(hari_buka),
        jam_buka=JSONEncoder().encode(jam_buka),
        status_book=JSONEncoder().encode(status_book)
    )

    new_jadwal.save()

    return new_jadwal


def updateTabelJadwal(request, id_sarana):

    try:
        Pengurus_GOR.objects.get(user=request.user)
    except:
        return HttpResponseForbidden()

    if request.method == 'POST':

        hari_buka_raw = request.POST.get('hari_buka')
        jam_buka_raw = request.POST.get('jam_buka')

        hari_buka = json.loads(hari_buka_raw)
        jam_buka = json.loads(jam_buka_raw)
        status_book = [[False for i in range(
            len(hari_buka))] for i in range(len(jam_buka))]

        jadwal = Sarana.objects.get(ID_sarana=id_sarana).id_jadwal

        new_jadwal = Jadwal_Reservasi(
            ID_jadwal=jadwal.ID_jadwal,
            hari_buka=JSONEncoder().encode(hari_buka),
            jam_buka=JSONEncoder().encode(jam_buka),
            status_book=JSONEncoder().encode(status_book)
        )

        new_jadwal.save()

    return render(request, 'trial.html')


def showTabelJadwal(request, id_sarana):

    context = {}

    if request.method == 'GET':

        jadwal = Sarana.objects.get(id=id_sarana).id_jadwal

        context = {
            'hari': jadwal.hari_buka,
            'jam': jadwal.jam_buka,
            'book': jadwal.status_book
        }

    return render(request, 'tabel_jadwal.html', context)


@login_required(login_url='/login/')
def getSaranaOlaharaga(request, ID_gor):
    if request.method == "GET":
        context = {}
        gor, created = GOR.objects.get_or_create(ID_gor=ID_gor)
        context = {"gor": gor, "daftar_sarana": gor.getSaranaGor()}
        return render(request, "sarana_olahraga.html", context)


@login_required(login_url='/login/')
def get_info_gor(request, ID_gor):
    if request.method == "GET":
        gor = GOR.objects.get(ID_gor=ID_gor)
        no_telp = gor.nomor_telepon
        if no_telp[0] == '0':
            no_telp = '62' + no_telp[1:]
        response = {'nama': gor.nama,
                    'url_foto': gor.url_foto,
                    'alamat': gor.alamat,
                    'no_telepon': gor.nomor_telepon,
                    'link_wa': "https://api.whatsapp.com/send?phone=" + no_telp}
        return render(request, 'info_gor.html', response)
