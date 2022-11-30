from django.db import models
from sarana_olahraga.models import Sarana
from pengguna.models import Konsumen_GOR, Pengurus_GOR


class Sewa_Sarana(models.Model):
    ID_sewa = models.TextField(primary_key=True)
    datetime = models.DateTimeField()
    sarana = models.ForeignKey(
        Sarana, on_delete=models.CASCADE, blank=True, null=True)
    biaya = models.FloatField()
    status = models.TextField()
    konsumen = models.ForeignKey(
        Konsumen_GOR, on_delete=models.CASCADE, blank=True, null=True)
    pengurus = models.ForeignKey(
        Pengurus_GOR, on_delete=models.CASCADE, blank=True, null=True)


class Detail_Pembayaran(models.Model):
    sewa_sarana = models.ForeignKey(
        Sewa_Sarana, on_delete=models.CASCADE, blank=True, null=True)
    datetime = models.DateTimeField()
    status = models.TextField()
    bukti_pembayaran = models.TextField()


class Pembatalan_Sewa_Sarana(models.Model):
    ID_pembatalan = models.TextField(primary_key=True)
    datetime = models.DateTimeField()
    pembatal = models.ForeignKey(
        Konsumen_GOR,  on_delete=models.CASCADE, blank=True, null=True)
    sewa_sarana = models.OneToOneField(
        Sewa_Sarana,  on_delete=models.CASCADE, blank=True, null=True)


class Verifikasi_Pembatalan(models.Model):
    datetime = models.DateTimeField()
    status = models.TextField()
    pembatalan = models.ForeignKey(
        Pembatalan_Sewa_Sarana,  on_delete=models.CASCADE, blank=True, null=True)
    pengurus = models.ForeignKey(
        Pengurus_GOR, on_delete=models.CASCADE, blank=True, null=True)
