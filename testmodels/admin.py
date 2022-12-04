from django.contrib import admin
from .models import Sewa_Sarana, Detail_Pembayaran, Pembatalan_Sewa_Sarana, Verifikasi_Pembatalan, Pengguna, Konsumen_GOR, Pengurus_GOR, GOR, Sarana, Jadwal_Reservasi, Status_Detail_Pembayaran, Status_Sewa_Sarana, Status_Verifikasi_Pembatalan

# Register your models here.
admin.site.register(Sewa_Sarana)
admin.site.register(Detail_Pembayaran)
admin.site.register(Pembatalan_Sewa_Sarana)
admin.site.register(Verifikasi_Pembatalan)
admin.site.register(Pengguna)
admin.site.register(Konsumen_GOR)
admin.site.register(Pengurus_GOR)
admin.site.register(GOR)
admin.site.register(Sarana)
admin.site.register(Jadwal_Reservasi)