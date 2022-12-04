from django.db import models
from django.contrib.auth.models import User


class Pengguna(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.TextField()
    nomor_telepon = models.TextField(unique=True)


class Konsumen_GOR(Pengguna):
    status_loyalty = models.TextField()


class Pengurus_GOR(Pengguna):
    akun_bank = models.TextField()
