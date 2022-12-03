from django.urls import path

from . import views

app_name = "sarana_olahraga"

urlpatterns = [
    path("<str:id_sarana>/jadwal", views.showTabelJadwal, name="show_tabel_jadwal"),
    path("<str:id_sarana>/update-jadwal", views.updateTabelJadwal, name="show_tabel_jadwal"),
]