from django.urls import path

from . import views

app_name = "reservasi_sarana"

urlpatterns = [
    path("reservasi/riwayat-reservasi", views.cekRiwayatReservasi, name="cek_riwayat_reservasi"),
]