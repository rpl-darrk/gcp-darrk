from django.urls import path

from . import views

app_name = "reservasi_sarana"

urlpatterns = [
    path("reservasi/verifikasi-pembayaran/<str:ID_sewa>",
         views.verifikasiPembayaran, name="verifikasi_pembayaran"),
    path("reservasi/verifikasi-pembatalan/<str:ID_sewa>",
         views.verifikasiPembatalan, name="verifikasi_pembatalan"),
    path("reservasi/pembatalan/<str:ID_sewa>",
         views.pembatalanReservasi, name="pembatalan"),
    path("reservasi/riwayat-reservasi",
         views.cekRiwayatReservasi, name="cek_riwayat_reservasi"),
    path('daftar-reservasi', views.get_daftar_reservasi,
         name='get_daftar_reservasi'),
    path('unggah-bukti-bayar', views.simpan_bukti_pembayaran,
         name='simpan_bukti_pembayaran')
]
