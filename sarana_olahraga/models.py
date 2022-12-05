from django.db import models
from pengguna.models import Pengurus_GOR


class GOR(models.Model):
    ID_gor = models.CharField(max_length=200, primary_key=True)
    nama = models.CharField(max_length=200)
    url_foto = models.CharField(max_length=200)
    alamat = models.CharField(max_length=200)
    nomor_telepon = models.CharField(max_length=200)
    pengurus = models.OneToOneField(
        Pengurus_GOR, on_delete=models.CASCADE, blank=True, null=True)

    def getSaranaGor(self):
        return self.sarana_set.all()


class Jadwal_Reservasi(models.Model):
    ID_jadwal = models.AutoField(primary_key=True)
    # array 1 dimensi boolean representasi hari
    hari_buka = models.JSONField(null=True)
    # array 2 dimensi string representasi waktu awal - waktu akhir
    jam_buka = models.JSONField(null=True)
    # array 2 dimensi boolean representasi status book pada pasangan hari & jam
    status_book = models.JSONField(null=True)


class Sarana(models.Model):
    class SaranaType(models.TextChoices):
        LAPANGAN_BASKET = "Lapangan Basket",
        LAPANGAN_BULU_TANGKIS = "Lapangan Bulutangkis",
        LAPANGAN_FUTSAL = "Lapangan Futsal",
        KOLAM_RENANG = "Kolam Renang",
        LAPANGAN_SEPAK_BOLA = "Lapangan Sepak Bola",

    gor = models.ForeignKey(to=GOR, on_delete=models.CASCADE)
    id_jadwal_reservasi = models.ForeignKey(
        to=Jadwal_Reservasi, on_delete=models.CASCADE)
    ID_sarana = models.CharField(max_length=200, primary_key=True)
    nama = models.CharField(max_length=200)
    url_foto = models.CharField(max_length=200)
    jenis = models.CharField(max_length=200, choices=SaranaType.choices)
    deskripsi = models.TextField(max_length=None)

    def get_sewa_sarana(self):
        return self.sewa_sarana_set.all()
