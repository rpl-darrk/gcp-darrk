from main.tests import FunctionalTestCase


class MainFunctionalTestCase(FunctionalTestCase):
    def test_root_url_exists(self):
        self.selenium.get(f"{self.live_server_url}/mengelola_sarana_olahraga")
        html = self.selenium.find_element_by_tag_name("html")
        self.assertNotIn("not found", html.text.lower())
        self.assertNotIn("error", html.text.lower())

    def test_post_url_exists(self):
        self.selenium.get(
            f"{self.live_server_url}/mengelola_sarana_olahraga/post_sarana")
        html = self.selenium.find_element_by_tag_name("html")
        self.assertNotIn("not found", html.text.lower())
        self.assertNotIn("error", html.text.lower())

    def test_update_url_exists(self):
        self.selenium.get(
            f"{self.live_server_url}/mengelola_sarana_olahraga/update_sarana/1")
        html = self.selenium.find_element_by_tag_name("html")
        self.assertNotIn("not found", html.text.lower())
        self.assertNotIn("error", html.text.lower())

    def test_delete_url_exists(self):
        self.selenium.get(
            f"{self.live_server_url}/mengelola_sarana_olahraga/delete_sarana/1")
        self.assertEqual(self.selenium.current_url,
                         f"{self.live_server_url}/mengelola_sarana_olahraga/")
