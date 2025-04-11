#!/usr/bin/env python
"""
Example script demonstrating how to create an EPUB with a navigation document.

This example creates a more complex EPUB with a proper navigation document
including a table of contents, page list, and landmarks.
"""

import os
import uuid
from datetime import datetime

from lxml import etree

from epub3 import EPUB, EPUBMetadata
from epub3.models import (
    ManifestItem,
    NavigationDocument,
    NavPoint,
    Resource,
    SpineItem,
    XHTMLDocument,
)


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


def create_navigation_document(toc_items, page_list_items, landmark_items):
    """Create a navigation document with TOC, page list, and landmarks."""
    nav_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>Navigation</title>
    <meta charset="utf-8" />
    <link rel="stylesheet" type="text/css" href="css/style.css" />
</head>
<body>
    <nav epub:type="toc" id="toc">
        <h2>Table of Contents</h2>
        <ol>
        </ol>
    </nav>

    <nav epub:type="page-list" id="page-list">
        <h2>List of Pages</h2>
        <ol>
        </ol>
    </nav>

    <nav epub:type="landmarks" id="landmarks">
        <h2>Landmarks</h2>
        <ol>
        </ol>
    </nav>
</body>
</html>"""

    # Create the navigation document
    nav_doc = NavigationDocument("nav", "nav.xhtml")
    parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
    dom = etree.fromstring(nav_content.encode("utf-8"), parser=parser)
    nav_doc.dom = etree.ElementTree(dom)

    # Add TOC items
    for item in toc_items:
        nav_doc.add_nav_point(item, "toc")

    # Add page list items
    for item in page_list_items:
        nav_doc.add_nav_point(item, "page-list")

    # Add landmark items
    for item in landmark_items:
        nav_doc.add_nav_point(item, "landmarks")

    return nav_doc


def main():
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Output path for the EPUB
    epub_path = os.path.join(output_dir, "book_with_navigation.epub")

    # Create an EPUB processor
    epub_processor = EPUB()

    # Create metadata
    metadata = EPUBMetadata(
        identifier=f"urn:uuid:{uuid.uuid4()}",
        title="Book with Navigation",
        language="en",
        creator=["Example Author"],
        publisher="Example Publisher",
        description="A demonstration of creating an EPUB with navigation",
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
h2 {
    color: #444;
    font-size: 1.5em;
    margin-top: 1.5em;
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
nav[epub|type="toc"] ol {
    list-style-type: none;
}
nav[epub|type="toc"] li {
    margin: 0.5em 0;
}
"""

    css_resource = Resource(
        id="style",
        path="css/style.css",
        media_type="text/css",
        data=css_content.encode("utf-8"),
    )
    epub.add_resource(css_resource)

    # Create and add the cover page
    cover_content = """
<div class="title-page">
    <h1>Book with Navigation</h1>
    <p class="author">by Example Author</p>
</div>
"""
    cover = create_content_document("cover", "Cover", cover_content, "cover.xhtml")
    epub_processor.add_content(epub, cover)

    # Create and add the title page
    title_page_content = """
<div class="title-page">
    <h1>Book with Navigation</h1>
    <p class="author">by Example Author</p>
    <p class="publisher">Example Publisher</p>
</div>
"""
    title_page = create_content_document(
        "title-page", "Title Page", title_page_content, "title-page.xhtml"
    )
    epub_processor.add_content(epub, title_page)

    # Create and add a copyright page
    copyright_content = """
<div>
    <h2>Copyright</h2>
    <p>© 2025 Example Publisher</p>
    <p>All rights reserved. No part of this book may be reproduced in any form
    without permission in writing from the publisher.</p>
</div>
"""
    copyright_page = create_content_document(
        "copyright", "Copyright", copyright_content, "copyright.xhtml"
    )
    epub_processor.add_content(epub, copyright_page)

    # Create and add a table of contents page (separate from navigation document)
    toc_content = """
<div>
    <h2>Contents</h2>
    <ul>
        <li><a href="chapter1.xhtml">Chapter 1: Introduction</a></li>
        <li><a href="chapter2.xhtml">Chapter 2: The Middle</a></li>
        <li><a href="chapter3.xhtml">Chapter 3: Conclusion</a></li>
    </ul>
</div>
"""
    toc_page = create_content_document(
        "contents", "Contents", toc_content, "contents.xhtml"
    )
    epub_processor.add_content(epub, toc_page)

    # Create and add chapters
    chapter1_content = """
<div epub:type="chapter">
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer nec odio.
    Praesent libero. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh
    elementum imperdiet. Duis sagittis ipsum. Praesent mauris. Fusce nec tellus
    sed augue semper porta. Mauris massa.</p>

    <h2 id="section1.1">1.1 First Section</h2>
    <p>Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora
    torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula
    in libero. Sed dignissim lacinia nunc. Curabitur tortor. Pellentesque nibh.
    Aenean quam. In scelerisque sem at dolor.</p>

    <h2 id="section1.2">1.2 Second Section</h2>
    <p>Maecenas mattis. Sed convallis tristique sem. Proin ut ligula vel nunc
    egestas porttitor. Morbi lectus risus, iaculis vel, suscipit quis, luctus non,
    massa. Fusce ac turpis quis ligula lacinia aliquet. Mauris ipsum. Nulla metus
    metus, ullamcorper vel, tincidunt sed, euismod in, nibh.</p>
</div>
"""
    chapter1 = create_content_document(
        "chapter1", "Chapter 1: Introduction", chapter1_content, "chapter1.xhtml"
    )
    epub_processor.add_content(epub, chapter1)

    chapter2_content = """
<div epub:type="chapter">
    <p>Quisque volutpat condimentum velit. Class aptent taciti sociosqu ad litora
    torquent per conubia nostra, per inceptos himenaeos. Nam nec ante. Sed lacinia,
    urna non tincidunt mattis, tortor neque adipiscing diam, a cursus ipsum ante
    quis turpis. Nulla facilisi. Ut fringilla. Suspendisse potenti. Nunc feugiat mi
    a tellus consequat imperdiet. Vestibulum sapien. Proin quam.</p>

    <h2 id="section2.1">2.1 First Section</h2>
    <p>Etiam ultrices. Suspendisse in justo eu magna luctus suscipit. Sed lectus.
    Integer euismod lacus luctus magna. Quisque cursus, metus vitae pharetra auctor,
    sem massa mattis sem, at interdum magna augue eget diam. Vestibulum ante ipsum
    primis in faucibus orci luctus et ultrices posuere cubilia Curae; Morbi lacinia
    molestie dui. Praesent blandit dolor.</p>

    <h2 id="section2.2">2.2 Second Section</h2>
    <p>Sed non quam. In vel mi sit amet augue congue elementum. Morbi in ipsum sit
    amet pede facilisis laoreet. Donec lacus nunc, viverra nec, blandit vel, egestas
    et, augue. Vestibulum tincidunt malesuada tellus. Ut ultrices ultrices enim.
    Curabitur sit amet mauris. Morbi in dui quis est pulvinar ullamcorper.</p>
</div>
"""
    chapter2 = create_content_document(
        "chapter2", "Chapter 2: The Middle", chapter2_content, "chapter2.xhtml"
    )
    epub_processor.add_content(epub, chapter2)

    chapter3_content = """
<div epub:type="chapter">
    <p>Nulla facilisi. Integer lacinia sollicitudin massa. Cras metus. Sed aliquet
    risus a tortor. Integer id quam. Morbi mi. Quisque nisl felis, venenatis
    tristique, dignissim in, ultrices sit amet, augue. Proin sodales libero eget
    ante. Nulla quam. Aenean laoreet. Vestibulum nisi lectus, commodo ac, facilisis
    ac, ultricies eu, pede. Ut orci risus, accumsan porttitor, cursus quis, aliquet
    eget, justo.</p>

    <h2 id="section3.1">3.1 First Section</h2>
    <p>Sed pretium blandit orci. Ut eu diam at pede suscipit sodales. Aenean lectus
    elit, fermentum non, convallis id, sagittis at, neque. Nullam mauris orci,
    aliquet et, iaculis et, viverra vitae, ligula. Nulla ut felis in purus aliquam
    imperdiet. Maecenas aliquet mollis lectus. Vivamus consectetuer risus et tortor.
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>

    <h2 id="section3.2">3.2 Second Section</h2>
    <p>Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi.
    Nulla quis sem at nibh elementum imperdiet. Duis sagittis ipsum. Praesent mauris.
    Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu
    eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra,
    per inceptos himenaeos.</p>
</div>
"""
    chapter3 = create_content_document(
        "chapter3", "Chapter 3: Conclusion", chapter3_content, "chapter3.xhtml"
    )
    epub_processor.add_content(epub, chapter3)

    # Create Navigation Points for TOC
    toc_items = [
        NavPoint("Cover", "cover.xhtml"),
        NavPoint("Title Page", "title-page.xhtml"),
        NavPoint("Copyright", "copyright.xhtml"),
        NavPoint("Contents", "contents.xhtml"),
        NavPoint(
            "Chapter 1: Introduction",
            "chapter1.xhtml",
            children=[
                NavPoint("1.1 First Section", "chapter1.xhtml#section1.1"),
                NavPoint("1.2 Second Section", "chapter1.xhtml#section1.2"),
            ],
        ),
        NavPoint(
            "Chapter 2: The Middle",
            "chapter2.xhtml",
            children=[
                NavPoint("2.1 First Section", "chapter2.xhtml#section2.1"),
                NavPoint("2.2 Second Section", "chapter2.xhtml#section2.2"),
            ],
        ),
        NavPoint(
            "Chapter 3: Conclusion",
            "chapter3.xhtml",
            children=[
                NavPoint("3.1 First Section", "chapter3.xhtml#section3.1"),
                NavPoint("3.2 Second Section", "chapter3.xhtml#section3.2"),
            ],
        ),
    ]

    # Create Navigation Points for Page List
    page_list_items = [
        NavPoint("1", "cover.xhtml"),
        NavPoint("2", "title-page.xhtml"),
        NavPoint("3", "copyright.xhtml"),
        NavPoint("4", "contents.xhtml"),
        NavPoint("5", "chapter1.xhtml"),
        NavPoint("6", "chapter1.xhtml#section1.1"),
        NavPoint("7", "chapter1.xhtml#section1.2"),
        NavPoint("8", "chapter2.xhtml"),
        NavPoint("9", "chapter2.xhtml#section2.1"),
        NavPoint("10", "chapter2.xhtml#section2.2"),
        NavPoint("11", "chapter3.xhtml"),
        NavPoint("12", "chapter3.xhtml#section3.1"),
        NavPoint("13", "chapter3.xhtml#section3.2"),
    ]

    # Create Navigation Points for Landmarks
    landmark_items = [
        NavPoint("Cover", "cover.xhtml"),
        NavPoint("Title Page", "title-page.xhtml"),
        NavPoint("Table of Contents", "contents.xhtml"),
        NavPoint("Begin Reading", "chapter1.xhtml"),
    ]

    # Create the navigation document
    nav_doc = create_navigation_document(toc_items, page_list_items, landmark_items)
    epub_processor.add_content(epub, nav_doc)

    # Set properties for the navigation document in the manifest
    nav_item = epub.manifest.get_item("nav")
    if nav_item:
        nav_item = ManifestItem(
            id="nav",
            href="nav.xhtml",
            media_type="application/xhtml+xml",
            properties=["nav"],
        )
        epub.manifest.remove_item("nav")
        epub.manifest.add_item(nav_item)

    # Set the navigation document
    epub.set_navigation_document(nav_doc)

    # Add items to the spine in the desired reading order
    epub.add_spine_item(SpineItem(idref="cover"))
    epub.add_spine_item(SpineItem(idref="title-page"))
    epub.add_spine_item(SpineItem(idref="copyright"))
    epub.add_spine_item(SpineItem(idref="contents"))
    epub.add_spine_item(SpineItem(idref="nav", linear="no"))  # Add nav as non-linear
    epub.add_spine_item(SpineItem(idref="chapter1"))
    epub.add_spine_item(SpineItem(idref="chapter2"))
    epub.add_spine_item(SpineItem(idref="chapter3"))

    # Write the EPUB to a file
    epub_processor.write(epub, epub_path)
    print(f"EPUB with navigation created successfully: {epub_path}")


if __name__ == "__main__":
    main()
