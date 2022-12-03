from django.db import models

from django.utils import timezone

from mengelola_sarana_olahraga.models import Sarana

class Status_Reservasi(models.Model):
    VACANT = 1
    ORDERED = 0

    Status = (
        (VACANT, "Vacant"),
        (ORDERED, "Ordered"),
    )

    status = models.IntegerField(choices=Status, default=VACANT)

class Jadwal_Reservasi(models.Model):
    id_jadwal = models.CharField(max_length=200, primary_key=True)
    id_sarana = models.ForeignKey(to=Sarana, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=9, default=Status_Reservasi.VACANT)
    datetime = models.DateField(default=timezone.now())
