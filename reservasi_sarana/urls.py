from django.urls import path

from . import views

app_name = "reservasi_sarana"

urlpatterns = [
    path("reservasi/verifikasi-pembayaran",
         views.verifikasiPembayaran, name="verifikasi_pembayaran"),
    path("reservasi/verifikasi-pembatalan",
         views.verifikasiPembatalan, name="verifikasi_pembatalan"),
    path("reservasi/pembatalan",
         views.pembatalanReservasi, name="pembatalan"),
    path("reservasi/selesai",
         views.selesaikanReservasi, name="pembatalan"),
    path("reservasi/riwayat-reservasi",
         views.cekRiwayatReservasi, name="cek_riwayat_reservasi"),
    path('daftar-reservasi', views.get_daftar_reservasi,
         name='get_daftar_reservasi'),
    path('unggah-bukti-bayar', views.simpan_bukti_pembayaran,
         name='simpan_bukti_pembayaran'),
    path("reservasi/<str:ID_gor>/<str:ID_sarana>/<str:waktu>",
         views.reservasi, name="buat_reservasi"),
    path("info-pembayaran/<str:ID_sewa>",
         views.detail_pembayaran, name="detail_bayar")
]
