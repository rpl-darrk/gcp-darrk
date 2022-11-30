from django.db import models
from pengguna.models import Pengurus_GOR


class GOR(models.Model):
    ID_gor = models.TextField(primary_key=True)
    nama = models.TextField()
    url_foto = models.TextField()
    alamat = models.TextField()
    no_telepon = models.TextField()
    pengurus = models.OneToOneField(
        Pengurus_GOR, on_delete=models.CASCADE, blank=True, null=True)


class Sarana(models.Model):
    ID_sarana = models.TextField(primary_key=True)
    nama = models.TextField()
    url_foto = models.TextField()
    jenis = models.TextField()
    deskripsi = models.TextField()
    gor = models.ForeignKey(
        GOR,  on_delete=models.CASCADE, blank=True, null=True)


class Jadwal_Reservasi(models.Model):
    ID_jadwal = models.TextField(primary_key=True)
    sarana = models.OneToOneField(
        Sarana,  on_delete=models.CASCADE, blank=True, null=True)
    status = models.TextField()
    datetime = models.DateTimeField()
