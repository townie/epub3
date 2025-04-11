"""Tests for the Resource models."""

import unittest

from epub3.models.resource import FontResource, Resource


class TestResource(unittest.TestCase):
    """Test case for Resource class."""

    def test_init(self):
        """Test initialization."""
        resource = Resource(
            id="test-id",
            path="test/path.html",
            media_type="text/html",
            data=b"<html></html>",
        )

        self.assertEqual(resource.id, "test-id")
        self.assertEqual(resource.path, "test/path.html")
        self.assertEqual(resource.media_type, "text/html")
        self.assertEqual(resource.get_data(), b"<html></html>")

    def test_get_text(self):
        """Test getting resource data as text."""
        resource = Resource(
            id="test-id",
            path="test/path.html",
            media_type="text/html",
            data=b"<html></html>",
        )

        self.assertEqual(resource.get_text(), "<html></html>")

    def test_set_data_bytes(self):
        """Test setting resource data as bytes."""
        resource = Resource(
            id="test-id",
            path="test/path.html",
            media_type="text/html",
            data=b"<html></html>",
        )

        resource.set_data(b"<html><body>Hello</body></html>")
        self.assertEqual(resource.get_data(), b"<html><body>Hello</body></html>")

    def test_set_data_str(self):
        """Test setting resource data as string."""
        resource = Resource(
            id="test-id",
            path="test/path.html",
            media_type="text/html",
            data=b"<html></html>",
        )

        resource.set_data("<html><body>Hello</body></html>")
        self.assertEqual(resource.get_text(), "<html><body>Hello</body></html>")


class TestFontResource(unittest.TestCase):
    """Test case for FontResource class."""

    def test_init(self):
        """Test initialization."""
        font = FontResource(
            id="font-id",
            path="fonts/test.ttf",
            media_type="font/ttf",
            data=b"font data",
            is_obfuscated=False,
        )

        self.assertEqual(font.id, "font-id")
        self.assertEqual(font.path, "fonts/test.ttf")
        self.assertEqual(font.media_type, "font/ttf")
        self.assertEqual(font.get_data(), b"font data")
        self.assertFalse(font.is_obfuscated)

    def test_obfuscation(self):
        """Test font obfuscation."""
        font = FontResource(
            id="font-id",
            path="fonts/test.ttf",
            media_type="font/ttf",
            data=b"font data",
        )

        # Initially not obfuscated
        self.assertFalse(font.is_obfuscated)

        # Obfuscate the font
        font.obfuscate()
        self.assertTrue(font.is_obfuscated)

        # Deobfuscate the font
        font.deobfuscate()
        self.assertFalse(font.is_obfuscated)


if __name__ == "__main__":
    unittest.main()
