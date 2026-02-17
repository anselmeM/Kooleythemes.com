import unittest
from playwright.sync_api import sync_playwright
import http.server
import threading
import socket
import time
import os

class ServerThread(threading.Thread):
    def __init__(self, directory):
        super().__init__(daemon=True)
        self.directory = directory
        self.httpd = None
        self.port = None
        self.started_event = threading.Event()

    def run(self):
        # Create handler with the specified directory
        def handler_factory(*args, **kwargs):
            return http.server.SimpleHTTPRequestHandler(*args, directory=self.directory, **kwargs)

        # Use port 0 to let the OS choose an available port
        self.httpd = http.server.HTTPServer(('127.0.0.1', 0), handler_factory)
        self.port = self.httpd.server_port
        self.started_event.set()
        self.httpd.serve_forever()

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()

class TestHomepageIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The root directory of the project
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.server_thread = ServerThread(root_dir)
        cls.server_thread.start()

        # Wait for server to start and pick a port
        if not cls.server_thread.started_event.wait(timeout=10):
            raise RuntimeError("Server failed to start")

        cls.port = cls.server_thread.port
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'browser'):
            cls.browser.close()
        if hasattr(cls, 'playwright'):
            cls.playwright.stop()
        if hasattr(cls, 'server_thread'):
            cls.server_thread.stop()

    def setUp(self):
        self.page = self.browser.new_page()
        # Block external resources (Facebook Pixel, AOS, Fonts) to ensure deterministic results
        def block_external(route):
            if any(domain in route.request.url for domain in ["facebook.net", "unpkg.com", "fonts.googleapis.com"]):
                route.abort()
            else:
                route.continue_()
        self.page.route("**/*", block_external)

    def tearDown(self):
        self.page.close()

    def test_homepage_title(self):
        """Verify the homepage has the correct title."""
        self.page.goto(f"http://127.0.0.1:{self.port}/Index.html", wait_until="domcontentloaded")
        self.assertEqual(self.page.title(), "Home")

    def test_homepage_sections(self):
        """Verify key sections exist and are visible."""
        self.page.goto(f"http://127.0.0.1:{self.port}/Index.html", wait_until="domcontentloaded")

        sections = [
            "nav.nav",
            "section.hero",
            "section.services",
            "section.about-us",
            "section.projects",
            "section.footer"
        ]

        for selector in sections:
            with self.subTest(selector=selector):
                # We use a small timeout for visibility check as we've blocked external resources
                is_visible = self.page.locator(selector).is_visible(timeout=5000)
                self.assertTrue(is_visible, f"Section {selector} should be visible")

if __name__ == "__main__":
    unittest.main()
