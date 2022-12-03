from django.urls import path
from .views import *

app_name = "jadwal_reservasi"

urlpatterns = [
    path("<id_jadwal>/", reservasi, name="reservasi"),
]
