from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from pengguna.models import Pengurus_GOR
from sarana_olahraga.models import GOR, Sarana, Jadwal_Reservasi
from sarana_olahraga.forms import SaranaForm

from .views_jadwal_reservasi import sinkronisasiDaftarTunggu

from json import JSONEncoder, loads

@login_required(login_url='/login/')
def index(request):
    pengurus_gor = Pengurus_GOR.objects.get(user=request.user)
    gor = GOR.objects.get(pengurus=pengurus_gor)
    sarana_list = Sarana.objects.filter(gor__ID_gor=gor.ID_gor)

    if len(sarana_list) == 0:
        sarana_list = None

    context = {
        'gor': gor,
        'sarana_list': sarana_list
    }
    return render(request, "mengelola_sarana_olahraga/index.html", context)


@login_required(login_url='/login/')
def add_sarana(request):
    if request.method == 'POST':
        form = SaranaForm(request.POST)
        if form.is_valid():
            sarana = form.save(commit=False)

            list_sarana = Sarana.objects.all()
            max_id = 0
            for saranaX in list_sarana:
                if int(saranaX.ID_sarana) > max_id:
                    max_id = int(saranaX.ID_sarana)

            sarana.ID_sarana = max_id + 1

            pengurus_gor = Pengurus_GOR.objects.get(user=request.user)
            sarana.gor = GOR.objects.get(pengurus=pengurus_gor)

            new_jadwal_reservasi = Jadwal_Reservasi.objects.create(
                hari_buka=[False, False, False, False, False, False, False],
                jam_buka=[],
                status_book=[],
            )
            new_jadwal_reservasi.save()

            sarana.id_jadwal_reservasi = new_jadwal_reservasi
            sarana.save()

            return HttpResponseRedirect('/mengelola-sarana-olahraga/')
    else:
        form = SaranaForm()

    return render(request, 'mengelola_sarana_olahraga/form.html', {'form': form})


@login_required(login_url='/login/')
def update_sarana(request, id_sarana):
    sarana = Sarana.objects.filter(ID_sarana=id_sarana).first()
    if sarana is not None:
        pengurus_gor = Pengurus_GOR.objects.get(user=request.user)
        gor = GOR.objects.get(pengurus=pengurus_gor)

        if sarana.gor == gor:
            if request.method == 'POST':
                form = SaranaForm(request.POST, instance=sarana)
                if form.is_valid():
                    sarana.save()
                    return HttpResponseRedirect('/mengelola-sarana-olahraga/')
            else:
                form = SaranaForm(instance=sarana)

            return render(request, 'mengelola_sarana_olahraga/form.html', {'form': form})

    return HttpResponseRedirect('/mengelola-sarana-olahraga//')


@login_required(login_url='/login/')
def delete_sarana(request, id_sarana):
    sarana = Sarana.objects.filter(ID_sarana=id_sarana).first()

    if sarana is not None:
        pengurus_gor = Pengurus_GOR.objects.get(user=request.user)
        gor = GOR.objects.get(pengurus=pengurus_gor)

        if sarana.gor == gor:
            sarana.id_jadwal_reservasi.delete()
            sarana.delete()

    return HttpResponseRedirect('/mengelola-sarana-olahraga/')


@login_required(login_url='/login/')
def aturTabelJadwal(request, id_sarana):
    
    try:
        Pengurus_GOR.objects.get(user=request.user)
    except:
        return HttpResponseForbidden()

    if request.method == 'GET':
        sarana = Sarana.objects.filter(ID_sarana=id_sarana).first()

        if sarana is not None:
            jadwal_reservasi = sarana.id_jadwal_reservasi

            hari_buka = jadwal_reservasi.hari_buka
            jam_buka = jadwal_reservasi.jam_buka
            status_book = jadwal_reservasi.status_book
            status_book_raw = [[False for i in range(7)] for j in range(len(status_book))]
            no_book = [True for i in range(7)]

            for i in range(len(status_book)):
                status_book[i].insert(0, jam_buka[i])
                for j in range(1, 8):
                    if not hari_buka[j - 1]:
                        status_book[i][j] = "Tutup"
                        status_book_raw[i][j-1] = True
                    elif not status_book[i][j]:
                        no_book[j-1] = False
                        status_book[i][j] = "Tidak Tersedia"
                        status_book_raw[i][j-1] = False
                    else:
                        status_book[i][j] = "Tersedia"
                        status_book_raw[i][j-1] = True

            daftar_tunggu = sarana.get_sewa_sarana().filter(status__exact=0)
            status_book = sinkronisasiDaftarTunggu(
                daftar_tunggu, status_book)

            context = {
                'id_sarana': id_sarana,
                'sarana': sarana,
                'hari_buka': hari_buka,
                'no_book': no_book,
                'status_book': status_book,
                'status_book_raw': status_book_raw
            }

            return render(request, 'mengatur_jadwal_reservasi.html', context)


@login_required(login_url='/login/')
def updateTabelJadwal(request, id_sarana):

    try:
        Pengurus_GOR.objects.get(user=request.user)
    except:
        return HttpResponseForbidden()

    if request.method == 'POST':

        hari_buka_raw = request.POST.get('hari_buka')
        jam_buka_raw = request.POST.get('jam_buka')
        status_book_raw = request.POST.get('status_book')
        status_book_raw = status_book_raw.replace("T", "t").replace("F", "f")

        hari_buka = loads(hari_buka_raw)
        jam_buka = loads(jam_buka_raw)
        status_book = loads(status_book_raw)

        for i in range(len(jam_buka)-len(status_book)):
            status_book.insert(len(status_book), [True, True, True, True, True, True, True])

        jadwal = Sarana.objects.get(ID_sarana=id_sarana).id_jadwal_reservasi

        new_jadwal = Jadwal_Reservasi(
            ID_jadwal=jadwal.ID_jadwal,
            hari_buka=hari_buka,
            jam_buka=jam_buka,
            status_book=status_book
        )

        new_jadwal.save()
        
        return HttpResponse(200)
