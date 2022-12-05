from django.test import TestCase, Client
from .views import *
from .models import *
from pengguna.models import *
from sarana_olahraga.models import *
from reservasi_sarana.models import *

class LihatDaftarReservasi(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user_pengurus = User.objects.create_user(
            email = "pengurus@email.com",
            username = "pengurus",
            password = "pengurus",
        )
        self.pengurus = Pengurus_GOR.objects.create(
            user = self.user_pengurus,
            nama = "pengurus",
            nomor_telepon = "081292929292",
            akun_bank = "000011112222"
        )
        self.user_konsumen = User.objects.create_user(
            email = "konsumen@email.com",
            username = "konsumen",
            password = "konsumen",
        )
        self.konsumen = Konsumen_GOR.objects.create(
            user = self.user_konsumen,
            nama = "konsumen",
            nomor_telepon = "081292929293",
            status_loyalty = "Basic Member"
        )
        self.user_konsumen2 = User.objects.create_user(
            email = "konsumen2@email.com",
            username = "konsumen2",
            password = "konsumen2",
        )
        self.konsumen2 = Konsumen_GOR.objects.create(
            user = self.user_konsumen2,
            nama = "konsumen2",
            nomor_telepon = "081292929294",
            status_loyalty = "Basic Member"
        )
        self.gor = GOR.objects.create(
            ID_gor = "1",
            nama = "nama",
            url_foto = "url_foto",
            alamat = "alamat", 
            no_telepon="081292929200", 
            pengurus=self.pengurus)
        self.sarana = Sarana.objects.create(
            ID_sarana = "2",
            nama = "sarana",
            url_foto = "gambar.jpg",
            jenis = "ABC",
            deskripsi = "deskripsi",
            gor=self.gor
        )
        self.sewa_sarana = Sewa_Sarana.objects.create(
            ID_sewa = "1",
            sarana = self.sarana,
            konsumen = self.konsumen,
            pengurus = self.pengurus
        )
        self.sewa_sarana = Sewa_Sarana.objects.create(
            ID_sewa = "2",
            sarana = self.sarana,
            konsumen = self.konsumen2,
            pengurus = self.pengurus
        )
    
    def test_get_daftar_reservasi(self):
        self.client.login(username = "pengurus", password = "pengurus")
        response = self.client.get("/daftar-reservasi")
        self.assertEqual(response.status_code, 200)