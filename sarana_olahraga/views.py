from django.shortcuts import render, redirect
from json import JSONEncoder

import json

from .models import Jadwal_Reservasi, Sarana

def initTabelJadwal():

    hari_buka = []
    jam_buka = [[]]
    status_book = [[False for i in range(len(hari_buka))] for i in range(len(jam_buka))]

    new_jadwal = Jadwal_Reservasi(
        hari_buka=JSONEncoder().encode(hari_buka), 
        jam_buka=JSONEncoder().encode(jam_buka), 
        status_book=JSONEncoder().encode(status_book)
    )

    return new_jadwal.save()


def updateTabelJadwal(request, id_sarana):

    if request.method == 'POST':

        hari_buka_raw = request.POST.get('hari_buka')
        jam_buka_raw = request.POST.get('jam_buka')

        hari_buka = json.loads(hari_buka_raw)
        jam_buka = json.loads(jam_buka_raw)
        status_book = [[False for i in range(len(hari_buka))] for i in range(len(jam_buka))]

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

    return render(request, '', context)