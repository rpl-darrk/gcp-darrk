from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from json import JSONEncoder
from django.contrib.auth.decorators import login_required

import json

from ..models import GOR, Jadwal_Reservasi, Sarana


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
        response = {'nama': gor.nama,
                    'url_foto': gor.url_foto,
                    'alamat': gor.alamat,
                    'no_telepon': gor.nomor_telepon}
        return render(request, 'info_gor.html', response)
