from django.db import models


class Sewa_Sarana(models.Model):
    ID_sewa = models.TextField()
    datetime = models.DateTimeField()
    biaya = models.FloatField()
    status = models.TextField()


class Detail_Pembayaran(models.Model):
    sewa_sarana = models.ForeignKey(Sewa_Sarana,  on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    status = models.TextField()
    bukti_pembayaran = models.TextField()


class Pembatalan_Sewa_Sarana(models.Model):
    ID_pembatalan = models.TextField()
    datetime = models.DateTimeField()
    sewa_sarana = models.ForeignKey(Sewa_Sarana,  on_delete=models.CASCADE)


class Verifikasi_Pembatalan(models.Model):
    datetime = models.DateTimeField()
    status = models.TextField()
    pembatalan = models.ForeignKey(
        Pembatalan_Sewa_Sarana,  on_delete=models.CASCADE)
