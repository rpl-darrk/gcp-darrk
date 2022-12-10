from django.urls import path
from ..view import views_mengelola_sarana

app_name = "mengelola_sarana_olahraga"

urlpatterns = [
    path("",
        views_mengelola_sarana.index, name="index"),
    path("add-sarana/",
        views_mengelola_sarana.add_sarana, name="add-sarana"),
    path("update-sarana/<str:id_sarana>",
         views_mengelola_sarana.update_sarana, name="update-sarana"),
    path("delete-sarana/<str:id_sarana>",
         views_mengelola_sarana.delete_sarana, name="delete-sarana"),
    path("atur-jadwal/<str:id_sarana>",
         views_mengelola_sarana.aturTabelJadwal, name="atur_tabel_jadwal"),
    path("update-jadwal/<str:id_sarana>",
         views_mengelola_sarana.updateTabelJadwal, name="update_tabel_jadwal"),
]
