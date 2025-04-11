# EPUB3 Library

A comprehensive Python library for reading, creating, modifying, and validating EPUB3 files according to the EPUB 3.3 specification.

## Overview

The EPUB3 library provides a robust and intuitive API for working with EPUB files. It encapsulates the complexity of the EPUB standard while offering a clean, object-oriented interface for developers.

### Key Features

- **Reading**: Parse and explore existing EPUB files
- **Creation**: Create new EPUB publications from scratch
- **Modification**: Update content, metadata, and structure of existing EPUBs
- **Validation**: Verify EPUB files against the specification
- **Navigation**: Work with tables of contents, landmarks, and page lists
- **Media**: Support for various media types and layouts

## Installation

```bash
# Install from repository
git clone https://github.com/username/epub3.git
cd epub3
pip install -e .

# Or simply install dependencies
pip install -r requirements.txt
```

## Usage Examples

### Reading an EPUB

```python
from epub3 import EPUB

# Open an EPUB file
epub_processor = EPUB()
epub = epub_processor.open("path/to/book.epub")

# Access metadata
print(f"Title: {epub.metadata.title}")
print(f"Author: {', '.join(epub.metadata.creator or [])}")

# Access navigation
nav = epub.navigation
if nav:
    print("Table of Contents:")
    for item in nav.toc:
        print(f"- {item.text} ({item.href})")

# Access content
for item in epub.spine.items:
    content_doc = epub.get_content_document(item.idref)
    if content_doc:
        print(f"Content: {content_doc.id}")
```

### Creating an EPUB

```python
from epub3 import EPUB, EPUBMetadata
from epub3.models import SpineItem, XHTMLDocument
import uuid
from datetime import datetime
from lxml import etree

# Create metadata
metadata = EPUBMetadata(
    identifier=f"urn:uuid:{uuid.uuid4()}",
    title="My New Book",
    language="en",
    creator=["Author Name"],
    modified=datetime.now()
)

# Create a new EPUB
epub_processor = EPUB()
epub = epub_processor.create(metadata)

# Create content
html_content = """<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Chapter 1</title></head>
<body><h1>Chapter 1</h1><p>Content here</p></body>
</html>"""

chapter = XHTMLDocument("chapter1", "chapter1.xhtml")
parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
dom = etree.fromstring(html_content.encode('utf-8'), parser=parser)
chapter.dom = etree.ElementTree(dom)

# Add content to EPUB
epub_processor.add_content(epub, chapter)

# Add to spine
epub.add_spine_item(SpineItem(idref="chapter1"))

# Write the EPUB
epub_processor.write(epub, "my_book.epub")
```

## Architecture

The library is designed around the following key components:

- **EPUB**: Main entry point for reading, creating, and writing EPUB files
- **EPUBContainer**: Represents a complete EPUB publication
- **PackageDocument**: Handles OPF package document (metadata, manifest, spine)
- **NavigationDocument**: Manages navigation (TOC, page lists, landmarks)
- **ContentDocument**: Base class for XHTML and SVG content
- **Resource**: Represents any resource within the EPUB

## More Examples

See the `examples` directory for more detailed usage examples:

- Creating an EPUB with navigation
- Modifying an existing EPUB
- Extracting content from an EPUB
- Validating an EPUB file

## Development

```bash
# Clone the repository
git clone https://github.com/username/epub3.git
cd epub3

# Install in development mode
pip install -e .

# Run tests
python -m unittest discover
```

## License

MIT
