from django.db import models
from pengguna.models import Konsumen_GOR, Pengurus_GOR

class Sewa_Sarana(models.Model):
    ID_sewa = models.TextField(primary_key=True)
    konsumen = models.ForeignKey(
        Konsumen_GOR, on_delete=models.CASCADE, blank=True, null=True)
    pengurus = models.ForeignKey(
        Pengurus_GOR, on_delete=models.CASCADE, blank=True, null=True)