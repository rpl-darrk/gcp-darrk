from django.db import models

class Jadwal_Reservasi(models.Model):
    ID_jadwal = models.AutoField(primary_key=True)
    hari_buka = models.JSONField() # array 1 dimensi boolean representasi hari
    jam_buka = models.JSONField() # array 2 dimensi string representasi waktu awal - waktu akhir
    status_book = models.JSONField() # array 2 dimensi boolean representasi status book pada pasangan hari & jam

class Sarana(models.Model):
    ID_sarana = models.TextField(primary_key=True)
    id_jadwal = models.ForeignKey(to=Jadwal_Reservasi, on_delete=models.CASCADE)