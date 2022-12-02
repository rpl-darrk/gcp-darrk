from django.shortcuts import render

from mengelola_sarana_olahraga.models import GOR, Sarana


# Create your views here.
def index(request):
    GORs = GOR.objects.all()
    saranas = Sarana.objects.all()
    print(GORs)
    context = {
        'GORs':GORs,
        'Saranas':saranas
    }
    return render(request, "index.html", context)
