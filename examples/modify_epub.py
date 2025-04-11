#!/usr/bin/env python
"""
Example script demonstrating how to read and modify an existing EPUB file.

This example opens an EPUB file, updates its metadata, adds a new chapter,
and writes it to a new file.
"""

import os
import sys
from datetime import datetime

from lxml import etree

from epub3 import EPUB, EPUBMetadata
from epub3.models import SpineItem, XHTMLDocument


def create_content_document(id, title, content, path):
    """Create an XHTML content document."""
    html_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>{title}</title>
    <meta charset="utf-8" />
</head>
<body>
    <h1>{title}</h1>
    {content}
</body>
</html>"""

    doc = XHTMLDocument(id, path)
    parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
    dom = etree.fromstring(html_content.encode("utf-8"), parser=parser)
    doc.dom = etree.ElementTree(dom)

    return doc


def main():
    # Check if an input EPUB file is provided
    if len(sys.argv) < 2:
        print("Usage: python modify_epub.py <path_to_epub>")
        print("Note: First create an EPUB using create_simple_epub.py")
        sys.exit(1)

    input_epub_path = sys.argv[1]
    if not os.path.exists(input_epub_path):
        print(f"Error: The file {input_epub_path} does not exist.")
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Output path for the modified EPUB
    epub_path = os.path.join(output_dir, "modified_book.epub")

    # Create an EPUB processor
    epub_processor = EPUB()

    try:
        # Open the existing EPUB
        epub = epub_processor.open(input_epub_path)

        # Display current metadata
        metadata = epub.metadata
        print("Current EPUB Metadata:")
        print(f"Title: {metadata.title}")
        print(f"Identifier: {metadata.identifier}")
        print(f"Creator(s): {', '.join(metadata.creator or [])}")
        print(f"Language: {metadata.language}")

        # Update metadata
        updated_metadata = EPUBMetadata(
            identifier=metadata.identifier,
            title=f"{metadata.title} - Modified",
            language=metadata.language,
            creator=metadata.creator,
            contributor=["Editor Name"] + (metadata.contributor or []),
            publisher=metadata.publisher,
            description="This is a modified version of the original EPUB",
            publication_date=metadata.publication_date,
            modified=datetime.now(),
            rights=metadata.rights,
        )

        # Update the EPUB metadata
        epub.update_metadata(updated_metadata)

        # Create a new chapter
        new_chapter_content = """
<p>This is a new chapter added to demonstrate how to modify an existing EPUB file.</p>

<p>The EPUB3 library makes it easy to read, modify, and write EPUB files with just
a few lines of Python code.</p>
"""
        new_chapter = create_content_document(
            "chapter3",
            "Chapter 3: Added Chapter",
            new_chapter_content,
            "chapter3.xhtml",
        )

        # Add the new chapter to the EPUB
        epub_processor.add_content(epub, new_chapter)

        # Add the new chapter to the spine (at the end)
        epub.add_spine_item(SpineItem(idref="chapter3"))

        # Write the modified EPUB to a new file
        epub_processor.write(epub, epub_path)
        print(f"\nModified EPUB created successfully: {epub_path}")

        # Display the changes made
        print("\nChanges made:")
        print(f"- Updated title to: {updated_metadata.title}")
        print(f"- Added contributor: {updated_metadata.contributor[0]}")
        print(f"- Added Chapter 3")
        print(f"- Updated modification date to: {updated_metadata.modified}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        # Clean up resources
        epub_processor.close()


if __name__ == "__main__":
    main()
