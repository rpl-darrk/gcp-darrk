from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from pengguna.models import Pengurus_GOR
from sarana_olahraga.models import GOR, Sarana, Jadwal_Reservasi
from sarana_olahraga.forms import SaranaForm


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
                hari_buka=[True, True, True, True, True, False, False],
                jam_buka=[["10.00", "11.00"], ["11.00", "12.00"]],
                status_book=[[True, True, True, True, True, True, True],
                             [True, True, True, True, True, True, True]],
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

