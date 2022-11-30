from django.contrib import admin
from .models import Sewa_Sarana, Detail_Pembayaran, Pembatalan_Sewa_Sarana, Verifikasi_Pembatalan

# Register your models here.
admin.site.register(Sewa_Sarana)
admin.site.register(Detail_Pembayaran)
admin.site.register(Pembatalan_Sewa_Sarana)
admin.site.register(Verifikasi_Pembatalan)
