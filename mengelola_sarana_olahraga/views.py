from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import GOR, Sarana
from .forms import SaranaForm


def index(request):
    sarana_list = Sarana.objects.all()
    context = {
        'sarana_list': sarana_list
    }
    return render(request, "mengelola_sarana_olahraga/index.html", context)


def post_sarana(request):
    if request.method == 'POST':
        form = SaranaForm(request.POST)
        if form.is_valid():
            sarana = form.save(commit=False)

            list_sarana = Sarana.objects.all()
            max_id = 0
            for saranaX in list_sarana:
                if int(saranaX.id) > max_id:
                    max_id = int(saranaX.id)

            sarana.id = max_id + 1
            sarana.gor = GOR.objects.get(id="1")
            sarana.save()

            return HttpResponseRedirect('/mengelola_sarana_olahraga/')
    else:
        form = SaranaForm()

    return render(request, 'mengelola_sarana_olahraga/form.html', {'form': form})


def update_sarana(request, id_sarana):
    sarana = Sarana.objects.filter(id=id_sarana).first()
    if sarana is not None:
        if request.method == 'POST':
            form = SaranaForm(request.POST, instance=sarana)
            if form.is_valid():
                sarana.save()
                return HttpResponseRedirect('/mengelola_sarana_olahraga/')
        else:
            form = SaranaForm(instance=sarana)

        return render(request, 'mengelola_sarana_olahraga/form.html', {'form': form})

    return HttpResponseRedirect('/mengelola_sarana_olahraga/')


def delete_sarana(request, id_sarana):
    sarana = Sarana.objects.filter(id=id_sarana).first()

    if sarana is not None:
        sarana.delete()

    return HttpResponseRedirect('/mengelola_sarana_olahraga/')
