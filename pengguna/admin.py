from django.contrib import admin
from .models import Pengguna, Konsumen_GOR, Pengurus_GOR

# Register your models here.
admin.site.register(Pengguna)
admin.site.register(Konsumen_GOR)
admin.site.register(Pengurus_GOR)
