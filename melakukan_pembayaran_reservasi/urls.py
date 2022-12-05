from django.urls import path
from .views import *

urlpatterns = [
    path('unggah-bukti-bayar', simpan_bukti_pembayaran, name='simpan_bukti_pembayaran')
]