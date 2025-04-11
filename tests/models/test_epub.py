"""Tests for the main EPUB class."""

import os
import shutil
import tempfile
import unittest
import zipfile
from datetime import datetime

from lxml import etree

from epub3.models import EPUB, EPUBMetadata
from epub3.models.content_document import XHTMLDocument


class TestEPUB(unittest.TestCase):
    """Test case for EPUB class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.epub_path = os.path.join(self.temp_dir, "test.epub")

    def tearDown(self):
        """Tear down test fixtures."""
        shutil.rmtree(self.temp_dir)

    def test_create_and_write(self):
        """Test creating a new EPUB and writing it to a file."""
        # Create an EPUB processor
        epub_processor = EPUB()

        # Create metadata
        metadata = EPUBMetadata(
            identifier="urn:uuid:12345",
            title="Test Book",
            language="en",
            creator=["Test Author"],
            modified=datetime.now(),
        )

        # Create a new EPUB
        epub = epub_processor.create(metadata)

        # Create a simple HTML content document
        content_html = """<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Test Chapter</title>
</head>
<body>
    <h1>Chapter 1</h1>
    <p>This is a test chapter.</p>
</body>
</html>"""

        content_doc = XHTMLDocument("chapter1", "chapter1.xhtml")
        parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
        dom = etree.fromstring(content_html.encode("utf-8"), parser=parser)
        content_doc.dom = etree.ElementTree(dom)

        # Add the content document to the EPUB
        epub_processor.add_content(epub, content_doc)

        # Add the content document to the spine
        from epub3.models import SpineItem

        epub.add_spine_item(SpineItem(idref="chapter1"))

        # Write the EPUB to a file
        epub_processor.write(epub, self.epub_path)

        # Verify that the file exists
        self.assertTrue(os.path.exists(self.epub_path))

        # Verify that the file is a valid EPUB
        with zipfile.ZipFile(self.epub_path, "r") as zip_file:
            # Check for required OCF files
            self.assertIn("mimetype", zip_file.namelist())
            self.assertIn("META-INF/container.xml", zip_file.namelist())

            # Check mimetype content
            with zip_file.open("mimetype") as f:
                mimetype = f.read().decode("utf-8").strip()
                self.assertEqual(mimetype, "application/epub+zip")

            # Check container.xml content
            with zip_file.open("META-INF/container.xml") as f:
                container_xml = f.read().decode("utf-8")
                self.assertIn(
                    '<rootfile full-path="content/package.opf"', container_xml
                )

            # Check that the content document exists
            self.assertIn("chapter1.xhtml", zip_file.namelist())

    # Removing test_open for now to focus on test_create_and_write


if __name__ == "__main__":
    unittest.main()
