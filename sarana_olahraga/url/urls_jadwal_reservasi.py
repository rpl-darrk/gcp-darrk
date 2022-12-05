from django.urls import path
from ..view import views_jadwal_reservasi

app_name = "jadwal_reservasi"

urlpatterns = [
    path("reservasi/<id_jadwal>/",
         views_jadwal_reservasi.reservasi, name="reservasi"),
    path("melihat_jadwal_reservasi/<str:id_gor>/<str:id_sarana>/",
         views_jadwal_reservasi.get_jadwal_reservasi, name="get_jadwal_reservasi"),
]
