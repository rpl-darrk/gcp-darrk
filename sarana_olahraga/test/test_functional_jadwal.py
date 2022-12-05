from main.tests import FunctionalTestCase


class MainFunctionalTestCase(FunctionalTestCase):
    def test_get_jadwal_reservasi_url_exists(self):
        self.selenium.get(
            f"{self.live_server_url}/melihat_jadwal_reservasi/1/1")
        html = self.selenium.find_element_by_tag_name("html")
        self.assertNotIn("not found", html.text.lower())
        self.assertNotIn("error", html.text.lower())
