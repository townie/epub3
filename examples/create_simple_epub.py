#!/usr/bin/env python
"""
Example script demonstrating how to create a simple EPUB file.

This example creates a basic EPUB with a title page and a couple of chapters.
"""

import os
import uuid
from datetime import datetime

from lxml import etree

from epub3 import EPUB, EPUBMetadata
from epub3.models import Resource, SpineItem, XHTMLDocument


def create_content_document(id, title, content, path):
    """Create an XHTML content document."""
    html_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>{title}</title>
    <meta charset="utf-8" />
    <link rel="stylesheet" type="text/css" href="css/style.css" />
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
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Output path for the EPUB
    epub_path = os.path.join(output_dir, "simple_book.epub")

    # Create an EPUB processor
    epub_processor = EPUB()

    # Create metadata
    metadata = EPUBMetadata(
        identifier=f"urn:uuid:{uuid.uuid4()}",
        title="My Simple Book",
        language="en",
        creator=["Example Author"],
        publisher="Example Publisher",
        description="A simple demonstration of creating an EPUB using the EPUB3 library",
        publication_date=datetime.now(),
        modified=datetime.now(),
        rights="© 2025 Example Publisher",
    )

    # Create a new EPUB
    epub = epub_processor.create(metadata)

    # Add a CSS stylesheet
    css_content = """
body {
    font-family: serif;
    margin: 2em;
    line-height: 1.5;
}
h1 {
    color: #333;
    text-align: center;
    font-size: 2em;
    margin-bottom: 1em;
}
p {
    margin-bottom: 0.5em;
    text-indent: 1.5em;
}
.title-page {
    text-align: center;
    margin-top: 30%;
}
.title-page h1 {
    font-size: 3em;
    margin-bottom: 2em;
}
.title-page .author {
    font-size: 1.5em;
    font-style: italic;
}
"""

    css_resource = Resource(
        id="style",
        path="css/style.css",
        media_type="text/css",
        data=css_content.encode("utf-8"),
    )
    epub.add_resource(css_resource)

    # Create and add the title page
    title_page_content = """
<div class="title-page">
    <h1>My Simple Book</h1>
    <p class="author">by Example Author</p>
</div>
"""
    title_page = create_content_document(
        "title-page", "My Simple Book", title_page_content, "title-page.xhtml"
    )
    epub_processor.add_content(epub, title_page)

    # Create and add Chapter 1
    chapter1_content = """
<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce euismod mattis mi,
id posuere lectus vestibulum vel. Morbi feugiat ipsum quis sem finibus elementum.
Aliquam finibus enim at est mattis, nec ultricies eros faucibus.</p>

<p>Ut consectetur ante in nulla iaculis feugiat. Pellentesque eget urna vel arcu
fringilla commodo. Proin blandit volutpat diam, rutrum finibus arcu sollicitudin nec.
Nam viverra fringilla ante, vel dignissim augue faucibus ac. Sed faucibus nisl quis
neque convallis viverra ac eu eros.</p>
"""
    chapter1 = create_content_document(
        "chapter1", "Chapter 1: Introduction", chapter1_content, "chapter1.xhtml"
    )
    epub_processor.add_content(epub, chapter1)

    # Create and add Chapter 2
    chapter2_content = """
<p>Pellentesque non convallis massa. Integer mattis pretium eros, ut bibendum arcu
facilisis vel. Ut consectetur, dui id volutpat molestie, felis mauris dictum arcu,
ac blandit nibh sem ac metus. Phasellus consectetur sem nibh, eu mattis libero
consectetur at.</p>

<p>Praesent ut tellus orci. Vivamus nunc velit, tincidunt vel blandit lacinia,
gravida a nisl. Quisque dictum, lectus eget faucibus aliquet, tortor augue molestie
tellus, id dapibus nisl leo non diam. Aliquam vitae justo elit. Duis gravida quam
vitae enim scelerisque mattis.</p>
"""
    chapter2 = create_content_document(
        "chapter2", "Chapter 2: Development", chapter2_content, "chapter2.xhtml"
    )
    epub_processor.add_content(epub, chapter2)

    # Add items to the spine in the desired reading order
    epub.add_spine_item(SpineItem(idref="title-page"))
    epub.add_spine_item(SpineItem(idref="chapter1"))
    epub.add_spine_item(SpineItem(idref="chapter2"))

    # Write the EPUB to a file
    epub_processor.write(epub, epub_path)
    print(f"EPUB created successfully: {epub_path}")


if __name__ == "__main__":
    main()
