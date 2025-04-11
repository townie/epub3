#!/usr/bin/env python
"""
Example script demonstrating how to extract content from an EPUB file.

This example extracts and displays the table of contents, metadata, and
the content of each document in the spine.
"""

import os
import sys

from lxml import etree

from epub3 import EPUB


def print_navigation(nav_points, level=0):
    """Print navigation points recursively with proper indentation."""
    for point in nav_points:
        indent = "  " * level
        print(f"{indent}- {point.text} ({point.href})")
        if point.children:
            print_navigation(point.children, level + 1)


def extract_text_from_html(html_content):
    """Extract readable text from HTML content."""
    root = etree.HTML(html_content)
    if root is None:
        return ""

    # Get all text blocks
    texts = root.xpath("//text()")

    # Filter and clean up the text
    cleaned_texts = []
    for text in texts:
        text = text.strip()
        if text:
            cleaned_texts.append(text)

    return "\n".join(cleaned_texts)


def main():
    # Check if an input EPUB file is provided
    if len(sys.argv) < 2:
        print("Usage: python extract_epub_content.py <path_to_epub>")
        sys.exit(1)

    input_epub_path = sys.argv[1]
    if not os.path.exists(input_epub_path):
        print(f"Error: The file {input_epub_path} does not exist.")
        sys.exit(1)

    # Create an EPUB processor
    epub_processor = EPUB()

    try:
        # Open the EPUB file
        epub = epub_processor.open(input_epub_path)

        # Extract and display metadata
        metadata = epub.metadata
        print("=" * 50)
        print("EPUB METADATA")
        print("=" * 50)
        print(f"Title: {metadata.title}")
        print(f"Identifier: {metadata.identifier}")
        if metadata.creator:
            print(f"Creator(s): {', '.join(metadata.creator)}")
        print(f"Language: {metadata.language}")
        if metadata.publisher:
            print(f"Publisher: {metadata.publisher}")
        if metadata.description:
            print(f"Description: {metadata.description}")
        if metadata.publication_date:
            print(f"Publication Date: {metadata.publication_date}")
        if metadata.modified:
            print(f"Last Modified: {metadata.modified}")
        if metadata.rights:
            print(f"Rights: {metadata.rights}")

        # Extract and display table of contents
        nav = epub.navigation
        if nav:
            print("\n" + "=" * 50)
            print("TABLE OF CONTENTS")
            print("=" * 50)
            print_navigation(nav.toc)

            # Print page list if available
            if nav.page_list:
                print("\n" + "=" * 50)
                print("PAGE LIST")
                print("=" * 50)
                print_navigation(nav.page_list)

            # Print landmarks if available
            if nav.landmarks:
                print("\n" + "=" * 50)
                print("LANDMARKS")
                print("=" * 50)
                print_navigation(nav.landmarks)

        # Extract and display text content from spine items
        print("\n" + "=" * 50)
        print("CONTENT")
        print("=" * 50)

        for i, spine_item in enumerate(epub.spine.items):
            # Get the content document
            content_doc = epub.get_content_document(spine_item.idref)
            if content_doc:
                print(
                    f"\n--- Document {i+1}: {spine_item.idref} ({content_doc.path}) ---\n"
                )

                # Save the document content
                content = content_doc.save().decode("utf-8")

                # Extract text and print
                text = extract_text_from_html(content)
                print(text[:500] + "..." if len(text) > 500 else text)
                print("\n" + "-" * 40)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        # Clean up resources
        epub_processor.close()


if __name__ == "__main__":
    main()
