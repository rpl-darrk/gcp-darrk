from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Pengguna(AbstractBaseUser):
    username = models.TextField(unique=True, primary_key=True)
    password = models.TextField()
    confirm_password = models.TextField()
    nama = models.TextField()
    email = models.EmailField(unique=True)
    nomor_telepon = models.EmailField(unique=True)


class Konsumen_GOR(Pengguna):
    status_loyalty = models.TextField()


class Pengurus_GOR(Pengguna):
    akun_bank = models.TextField()
