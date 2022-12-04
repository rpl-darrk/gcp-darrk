from django.db import models


class JadwalReservasi(models.Model):
    id = models.AutoField(primary_key=True)
    hari_buka = models.JSONField()
    jam_buka = models.JSONField()
    status_book = models.JSONField()
