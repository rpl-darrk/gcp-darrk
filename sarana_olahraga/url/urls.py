from django.urls import path

from sarana_olahraga.view import views

app_name = "sarana_olahraga"

urlpatterns = [
    path("<str:id_sarana>/jadwal", 
        views.showTabelJadwal, name="show_tabel_jadwal"),
    path("sarana/<str:ID_gor>", 
        views.getSaranaOlaharaga, name="sarana_olahraga"),
    path('info-gor/<str:ID_gor>', 
        views.get_info_gor, name='get_info_gor')
]
