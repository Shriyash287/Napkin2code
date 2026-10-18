"""Integration checks for resources served from the separated frontend."""
import os
import tempfile
import unittest
from pathlib import Path

from backend import config
from backend.app import app


class ArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_frontend_assets_and_sample_are_served(self):
        for path, mime in [
            ("/static/app.js", "javascript"),
            ("/static/style.css", "text/css"),
            ("/static/logo.svg", "image/svg+xml"),
            ("/static/icons.svg", "image/svg+xml"),
            ("/samples/login-sketch.png", "image/png"),
        ]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertIn(mime, response.content_type)
                self.assertGreater(len(response.data), 0)
                response.close()

    def test_resources_resolve_outside_project_working_directory(self):
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as folder:
            try:
                os.chdir(folder)
                self.assertEqual(self.client.get("/scan").status_code, 200)
                response = self.client.get("/samples/login-sketch.png")
                self.assertEqual(response.status_code, 200)
                response.close()
                self.assertEqual(Path(app.template_folder), config.FRONTEND_DIR / "templates")
                self.assertEqual(Path(app.static_folder), config.FRONTEND_DIR / "static")
            finally:
                os.chdir(previous)

    def test_private_backend_files_are_not_public_resources(self):
        for path in ["/.env", "/.model.json", "/backend/config.py", "/static/../.env"]:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 404)
