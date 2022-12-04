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

    def getSaranaGor(self):
        return self.sarana_set.all()


class Sarana(models.Model):
    ID_sarana = models.TextField(primary_key=True)
    id_jadwal = models.ForeignKey(to=Jadwal_Reservasi, on_delete=models.CASCADE)
    nama = models.TextField()
    url_foto = models.TextField()
    jenis = models.TextField()
    deskripsi = models.TextField()
    gor = models.ForeignKey(
        GOR, on_delete=models.CASCADE, blank=True, null=True)


class Jadwal_Reservasi(models.Model):
    ID_jadwal = models.AutoField(primary_key=True)
    hari_buka = models.JSONField() # array 1 dimensi boolean representasi hari
    jam_buka = models.JSONField() # array 2 dimensi string representasi waktu awal - waktu akhir
    status_book = models.JSONField() # array 2 dimensi boolean representasi status book pada pasangan hari & jam
