# EPUB3 Library Examples

This directory contains example scripts demonstrating how to use the EPUB3 library for various operations.

## Setup

Before running the examples, make sure you have installed the EPUB3 library:

```bash
cd /path/to/epub3
pip install -e .
```

## Available Examples

### 1. Create a Simple EPUB

**Script**: `create_simple_epub.py`

Creates a basic EPUB with a title page and a couple of chapters.

```bash
python create_simple_epub.py
```

Output is saved to `output/simple_book.epub`.

### 2. Create an EPUB with Navigation

**Script**: `create_epub_with_navigation.py`

Creates a more complex EPUB with a proper navigation document including a table of contents, page list, and landmarks.

```bash
python create_epub_with_navigation.py
```

Output is saved to `output/book_with_navigation.epub`.

### 3. Modify an Existing EPUB

**Script**: `modify_epub.py`

Demonstrates how to read and modify an existing EPUB file. Updates metadata, adds a new chapter, and writes to a new file.

```bash
# First create an EPUB to modify
python create_simple_epub.py

# Then modify it
python modify_epub.py output/simple_book.epub
```

Output is saved to `output/modified_book.epub`.

### 4. Extract EPUB Content

**Script**: `extract_epub_content.py`

Extracts and displays the table of contents, metadata, and content of each document in the spine.

```bash
python extract_epub_content.py path/to/some/book.epub
```

### 5. Validate an EPUB

**Script**: `validate_epub.py`

Validates an EPUB file and reports any errors or warnings.

```bash
python validate_epub.py path/to/some/book.epub
```

## Output Directory

The examples that create EPUB files will save them to an `output` directory within the `examples` folder. This directory will be created automatically if it doesn't exist.

## Notes

- These examples demonstrate the basic functionality of the EPUB3 library.
- Real-world usage might require additional error handling and configuration.
- The library supports more advanced features not shown in these examples, such as fixed layouts, media overlays, and advanced metadata handling.
