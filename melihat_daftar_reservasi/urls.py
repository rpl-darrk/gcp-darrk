from django.urls import path
from .views import *

urlpatterns = [
    path('daftar-reservasi', get_daftar_reservasi, name='get_daftar_reservasi')
]