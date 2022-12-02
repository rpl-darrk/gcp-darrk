from django.test import TestCase, Client
from jadwal_reservasi.models import Jadwal_Reservasi, Status_Reservasi

def ReservasiJadwalTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.jadwal_reservasi = Jadwal_Reservasi.objects.create(id_jadwal=0)
    
    def test_status_after_reservation(self):
        assert(self.jadwal_reservasi.status.__eq__(Status_Reservasi.VACANT))
        response = self.client.post("/reservasi/0")
        assert(response.status_code.__eq__(302))
        assert(self.jadwal_reservasi.status.__eq__(Status_Reservasi.ORDERED))