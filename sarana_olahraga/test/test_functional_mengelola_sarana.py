from main.tests import FunctionalTestCase


class MainFunctionalTestCase(FunctionalTestCase):
    def test_root_url_exists(self):
        self.selenium.get(f"{self.live_server_url}/mengelola-sarana-olahraga")
        html = self.selenium.find_element_by_tag_name("html")
        self.assertNotIn("not found", html.text.lower())
        self.assertNotIn("error", html.text.lower())

    def test_post_url_exists(self):
        self.selenium.get(
            f"{self.live_server_url}/mengelola-sarana-olahraga/add-sarana")
        html = self.selenium.find_element_by_tag_name("html")
        self.assertNotIn("not found", html.text.lower())
        self.assertNotIn("error", html.text.lower())

    def test_update_url_exists(self):
        self.selenium.get(
            f"{self.live_server_url}/mengelola-sarana-olahraga/update-sarana/1")
        html = self.selenium.find_element_by_tag_name("html")
        self.assertNotIn("not found", html.text.lower())
        self.assertNotIn("error", html.text.lower())

    def test_delete_url_exists(self):
        self.selenium.get(
            f"{self.live_server_url}/mengelola-sarana-olahraga/delete-sarana/1")
        self.assertEqual(self.selenium.current_url,
                         f"{self.live_server_url}/login/?next=/mengelola-sarana-olahraga/delete-sarana/1")
