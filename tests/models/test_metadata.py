"""Tests for the EPUBMetadata model."""

import unittest
from datetime import datetime

from epub3.models.metadata import EPUBMetadata


class TestEPUBMetadata(unittest.TestCase):
    """Test case for EPUBMetadata class."""

    def test_init_with_required_fields(self):
        """Test initialization with just the required fields."""
        metadata = EPUBMetadata(
            identifier="urn:uuid:12345", title="Test Book", language="en"
        )

        self.assertEqual(metadata.identifier, "urn:uuid:12345")
        self.assertEqual(metadata.title, "Test Book")
        self.assertEqual(metadata.language, "en")
        self.assertIsNone(metadata.creator)
        self.assertIsNone(metadata.contributor)
        self.assertIsNone(metadata.publisher)
        self.assertIsNone(metadata.description)
        self.assertIsNone(metadata.publication_date)
        self.assertIsNone(metadata.modified)
        self.assertIsNone(metadata.rights)
        self.assertEqual(metadata.extra, {})

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        now = datetime.now()
        metadata = EPUBMetadata(
            identifier="urn:uuid:12345",
            title="Test Book",
            language="en",
            creator=["Author One", "Author Two"],
            contributor=["Contributor"],
            publisher="Test Publisher",
            description="A test book",
            publication_date=now,
            modified=now,
            rights="All rights reserved",
            extra={"custom": "value"},
        )

        self.assertEqual(metadata.identifier, "urn:uuid:12345")
        self.assertEqual(metadata.title, "Test Book")
        self.assertEqual(metadata.language, "en")
        self.assertEqual(metadata.creator, ["Author One", "Author Two"])
        self.assertEqual(metadata.contributor, ["Contributor"])
        self.assertEqual(metadata.publisher, "Test Publisher")
        self.assertEqual(metadata.description, "A test book")
        self.assertEqual(metadata.publication_date, now)
        self.assertEqual(metadata.modified, now)
        self.assertEqual(metadata.rights, "All rights reserved")
        self.assertEqual(metadata.extra, {"custom": "value"})

    def test_missing_required_fields(self):
        """Test that an error is raised when required fields are missing."""
        with self.assertRaises(ValueError):
            EPUBMetadata(identifier="", title="Test", language="en")

        with self.assertRaises(ValueError):
            EPUBMetadata(identifier="test", title="", language="en")

        with self.assertRaises(ValueError):
            EPUBMetadata(identifier="test", title="Test", language="")


if __name__ == "__main__":
    unittest.main()
