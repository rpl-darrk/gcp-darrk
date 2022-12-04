# Models code taken/copied from Ramdhan's apps for testing purposes only.
# This "testmodels" app will be deleted and overall code will be adjusted before integration.

from django.db import models
from django.contrib.auth.models import User

class Pengguna(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.TextField()
    nomor_telepon = models.TextField(unique=True)


class Konsumen_GOR(Pengguna):
    status_loyalty = models.TextField()


class Pengurus_GOR(Pengguna):
    akun_bank = models.TextField()

from django.db import models

class GOR(models.Model):
    ID_gor = models.TextField(primary_key=True)
    nama = models.TextField()
    url_foto = models.TextField()
    alamat = models.TextField()
    no_telepon = models.TextField()
    pengurus = models.OneToOneField(
        Pengurus_GOR, on_delete=models.CASCADE, blank=True, null=True)

    def getSaranaGor(self):
        return self.sarana_set.all()


class Sarana(models.Model):
    ID_sarana = models.TextField(primary_key=True)
    nama = models.TextField()
    url_foto = models.TextField()
    jenis = models.TextField()
    deskripsi = models.TextField()
    gor = models.ForeignKey(
        GOR, on_delete=models.CASCADE, blank=True, null=True)


class Jadwal_Reservasi(models.Model):
    ID_jadwal = models.TextField(primary_key=True)
    sarana = models.OneToOneField(
        Sarana,  on_delete=models.CASCADE, blank=True, null=True)
    status = models.TextField()
    datetime = models.DateTimeField()

class Status_Sewa_Sarana(models.Model):
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


class Status_Detail_Pembayaran(models.Model):
    NOTYET = 0
    WAITING = 1
    VERIFIED = 2

    Status = (
        (NOTYET, "Belum upload bukti pembayaran"),
        (WAITING, "Menunggu verifikasi bukti pembayaran"),
        (VERIFIED, "Pembayaran terverifikasi"),
    )

    status = models.IntegerField(choices=Status, default=NOTYET)


class Status_Verifikasi_Pembatalan(models.Model):
    SUBMITTED = 0
    VERIFIED = 1

    Status = (
        (SUBMITTED, "Pembatalan diajukan"),
        (VERIFIED, "Pembatalan terverifikasi"),
    )

    status = models.IntegerField(choices=Status, default=SUBMITTED)


class Sewa_Sarana(models.Model):
    ID_sewa = models.TextField(primary_key=True)
    datetime = models.DateTimeField(auto_now_add=True)
    sarana = models.ForeignKey(
        Sarana, on_delete=models.CASCADE, blank=True, null=True)
    biaya = models.FloatField(default=0)
    status = models.TextField(default=Status_Sewa_Sarana.WAITTOPAY)
    konsumen = models.ForeignKey(
        Konsumen_GOR, on_delete=models.CASCADE, blank=True, null=True)
    pengurus = models.ForeignKey(
        Pengurus_GOR, on_delete=models.CASCADE, blank=True, null=True)

    def ubahStatusPembayaran(self, status):
        detail_pembayaran, created = Detail_Pembayaran.objects.get_or_create(
            sewa_sarana=self)
        if status == Status_Detail_Pembayaran.VERIFIED:
            self.updateStatus(Status_Sewa_Sarana.PAID)
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
            self.updateStatus(Status_Sewa_Sarana.CANCELLED)

    def updateStatus(self, status):
        self.status = status
        self.save()


class Detail_Pembayaran(models.Model):
    sewa_sarana = models.ForeignKey(
        Sewa_Sarana, on_delete=models.CASCADE, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.TextField(default=Status_Detail_Pembayaran.NOTYET)
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
    status = models.TextField(default=Status_Verifikasi_Pembatalan.SUBMITTED)
    pembatalan = models.ForeignKey(
        Pembatalan_Sewa_Sarana,  on_delete=models.CASCADE, blank=True, null=True)
    pengurus = models.ForeignKey(
        Pengurus_GOR, on_delete=models.CASCADE, blank=True, null=True)

    def verifikasiPembatalan(self):
        self.status = Status_Verifikasi_Pembatalan.VERIFIED
        self.save()