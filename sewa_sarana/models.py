from django.db import models
from mengelola_sarana_olahraga.models import Sarana


class StatusSewaSarana(models.Model):
    WAITTOPAY = 0
    PAID = 1
    CANCELLED = 2
    DONE = 3

    Status = (
        (WAITTOPAY, "Menunggu pembayaran"),
        (PAID, "Berhasil dibayar"),
        (CANCELLED, "Batal"),
        (DONE, "Selesai"),
    )

    status = models.IntegerField(choices=Status, default=WAITTOPAY)


class SewaSarana(models.Model):
    ID_sewa = models.TextField(primary_key=True)
    datetime = models.DateTimeField(auto_now_add=True)
    sarana = models.ForeignKey(Sarana, on_delete=models.CASCADE, blank=True, null=True)
    status = models.TextField(default=StatusSewaSarana.WAITTOPAY)
    jam_booking = models.JSONField()
