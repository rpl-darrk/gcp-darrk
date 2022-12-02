from django.db import models
from sarana_olahraga.models import Sarana
from pengguna.models import Pengguna, Konsumen_GOR, Pengurus_GOR


class Sewa_Sarana(models.Model):
    ID_sewa = models.TextField(primary_key=True)
    datetime = models.DateTimeField(auto_now_add=True)
    sarana = models.ForeignKey(
        Sarana, on_delete=models.CASCADE, blank=True, null=True)
    biaya = models.FloatField(default=0)
    status = models.TextField(default="Menunggu pembayaran")
    konsumen = models.ForeignKey(
        Konsumen_GOR, on_delete=models.CASCADE, blank=True, null=True)
    pengurus = models.ForeignKey(
        Pengurus_GOR, on_delete=models.CASCADE, blank=True, null=True)

    def ubahStatusPembayaran(self, status):
        detail_pembayaran, created = Detail_Pembayaran.objects.get_or_create(
            sewa_sarana=self)
        if status == "Pembayaran terverifikasi":
            self.updateStatus("Berhasil dibayar")
        detail_pembayaran.ubahStatusDetailPembayaran(status)

    def batalSewa(self, pembatal):
        pembatalan = Pembatalan_Sewa_Sarana.objects.create(
            sewa_sarana=self, pembatal=pembatal)
        verifikasi = Verifikasi_Pembatalan.objects.create(
            pembatalan=pembatalan, pengurus=self.pengurus)

        try:
            pengurus = Pengurus_GOR.objects.get(
                user=pembatal.user)
        except Pengurus_GOR.DoesNotExist:
            pengurus = None

        if pengurus is not None:
            verifikasi.verifikasiPembatalan()
            self.updateStatus("Batal")

    def updateStatus(self, status):
        self.status = status
        self.save()


class Detail_Pembayaran(models.Model):
    sewa_sarana = models.ForeignKey(
        Sewa_Sarana, on_delete=models.CASCADE, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.TextField()
    bukti_pembayaran = models.TextField(blank=True, null=True)

    def ubahStatusDetailPembayaran(self, status):
        self.status = status
        self.save()


class Pembatalan_Sewa_Sarana(models.Model):
    ID_pembatalan = models.TextField(primary_key=True)
    datetime = models.DateTimeField(auto_now_add=True)
    pembatal = models.ForeignKey(
        Pengguna,  on_delete=models.CASCADE, blank=True, null=True)
    sewa_sarana = models.OneToOneField(
        Sewa_Sarana,  on_delete=models.CASCADE, blank=True, null=True)


class Verifikasi_Pembatalan(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.TextField(default="Pembatalan diajukan")
    pembatalan = models.ForeignKey(
        Pembatalan_Sewa_Sarana,  on_delete=models.CASCADE, blank=True, null=True)
    pengurus = models.ForeignKey(
        Pengurus_GOR, on_delete=models.CASCADE, blank=True, null=True)

    def verifikasiPembatalan(self):
        self.status = "Pembatalan terverifikasi"
        self.save()
