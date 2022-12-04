from django.urls import path
from . import views

app_name = "melihat_jadwal_reservasi"

urlpatterns = [
    path("<str:id_gor>/<str:id_sarana>/", views.get_jadwal_reservasi, name="get_jadwal_reservasi"),
]
