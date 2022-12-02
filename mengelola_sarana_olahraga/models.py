from django.db import models


# Create your models here.
class GOR(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    nama = models.CharField(max_length=200)
    url_foto = models.CharField(max_length=200)
    alamat = models.CharField(max_length=200)
    nomor_telepon = models.CharField(max_length=200)


class Sarana(models.Model):
    id_gor = models.ForeignKey(to=GOR, on_delete=models.CASCADE)
    id = models.CharField(max_length=200, primary_key=True)
    url_foto = models.CharField(max_length=200)
    jenis = models.CharField(max_length=200)
    deskripsi = models.TextField(max_length=None)
