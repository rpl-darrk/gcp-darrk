from django.db import models
from melihat_jadwal_reservasi.models import JadwalReservasi

class GOR(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    nama = models.CharField(max_length=200)
    url_foto = models.CharField(max_length=200)
    alamat = models.CharField(max_length=200)
    nomor_telepon = models.CharField(max_length=200)


class Sarana(models.Model):
    class SaranaType(models.TextChoices):
        LAPANGAN_BASKET = "Lapangan Basket",
        LAPANGAN_BULU_TANGKIS = "Lapangan Bulutangkis",
        LAPANGAN_FUTSAL = "Lapangan Futsal",
        KOLAM_RENANG = "Kolam Renang",
        LAPANGAN_SEPAK_BOLA = "Lapangan Sepak Bola",

    gor = models.ForeignKey(to=GOR, on_delete=models.CASCADE)
    jadwal_reservasi = models.ForeignKey(to=JadwalReservasi, on_delete=models.CASCADE)
    id = models.CharField(max_length=200, primary_key=True)
    nama = models.CharField(max_length=200)
    url_foto = models.CharField(max_length=200)
    jenis = models.CharField(max_length=200, choices=SaranaType.choices)
    deskripsi = models.TextField(max_length=None)

    def get_sewa_sarana(self):
        return self.sewasarana_set.all()