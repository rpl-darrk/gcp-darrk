from django.test import TestCase, Client
from .views import *
from .models import *
from pengguna.models import *
from sarana_olahraga.models import *
from reservasi_sarana.models import *

class GetInfoGORTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user_konsumen = User.objects.create_user(
            email = "konsumen@email.com",
            username = "konsumen",
            password = "konsumen",
        )
        self.konsumen = Konsumen_GOR.objects.create(
            user = self.user_konsumen,
            nama = "konsumen",
            nomor_telepon = "081292929292",
            status_loyalty = "Basic Member"
        )
        self.user_pengurus = User.objects.create_user(
            email = "pengurus@email.com",
            username = "pengurus",
            password = "pengurus",
        )
        self.pengurus = Pengurus_GOR.objects.create(
            user = self.user_pengurus,
            nama = "pengurus",
            nomor_telepon = "081299999999",
            akun_bank = "000011112222"
        )
        self.gor = GOR.objects.create(
            ID_gor = "1",
            nama = "nama",
            url_foto = "url_foto",
            alamat = "alamat", 
            no_telepon="081292929200",
            pengurus=self.pengurus
        )
    
    def test_get_info_gor(self):
        self.client.login(username = "konsumen", password = "konsumen")
        response = self.client.get("/info-gor/1")
        self.assertEqual(response.status_code, 200)