# EPUB3 Library - High-Level API

This document outlines the high-level classes and APIs for the EPUB3 library based on the implementation tasks.

## Core Classes

### `EPUB`

Primary class for reading, parsing, creating, and writing EPUB files.

```python
from typing import Optional, Union, BinaryIO, Dict, Any

class EPUB:
    def __init__(self, options: Optional[dict] = None):
        """Initialize the EPUB processor with optional configuration."""
        pass

    # Reading operations
    def open(self, source: Union[str, BinaryIO, bytes]) -> "EPUBContainer":
        """Open an EPUB file from a file path, file-like object, or bytes."""
        pass

    # Creation operations
    def create(self, metadata: "EPUBMetadata") -> "EPUBContainer":
        """Create a new EPUB container with the provided metadata."""
        pass

    # Writing operations
    def write(self, epub: "EPUBContainer", destination: Union[str, BinaryIO]) -> None:
        """Write the EPUB to a file path or file-like object."""
        pass

    def add_content(self, epub: "EPUBContainer", content: "EPUBContent") -> None:
        """Add content to the EPUB container."""
        pass

    # Validation operations
    def validate(self, epub: "EPUBContainer") -> "ValidationResult":
        """Validate the EPUB file against the EPUB specification."""
        pass

    # Resource management
    def close(self) -> None:
        """Close and clean up any resources."""
        pass
```

### `EPUBContainer`

Represents an EPUB publication with all its components.

```python
from typing import Optional, List, Dict, Any, Union

class EPUBContainer:
    @property
    def metadata(self) -> "EPUBMetadata":
        """Get the EPUB metadata."""
        pass

    @property
    def manifest(self) -> "EPUBManifest":
        """Get the EPUB manifest."""
        pass

    @property
    def spine(self) -> "EPUBSpine":
        """Get the EPUB spine."""
        pass

    @property
    def navigation(self) -> "EPUBNavigation":
        """Get the EPUB navigation."""
        pass

    # Core operations
    def get_package_document(self) -> "PackageDocument":
        """Get the package document."""
        pass

    def get_content_document(self, id: str) -> "ContentDocument":
        """Get a content document by ID."""
        pass

    def get_navigation(self) -> "NavigationDocument":
        """Get the navigation document."""
        pass

    # Resource management
    def get_resource(self, path: str) -> "Resource":
        """Get a resource by path."""
        pass

    def add_resource(self, resource: "Resource") -> None:
        """Add a resource to the EPUB."""
        pass

    def remove_resource(self, path: str) -> None:
        """Remove a resource from the EPUB."""
        pass

    # Content modification
    def update_metadata(self, metadata: Dict[str, Any]) -> None:
        """Update the EPUB metadata."""
        pass

    def add_spine_item(self, item: "SpineItem", index: Optional[int] = None) -> None:
        """Add an item to the spine."""
        pass

    def remove_spine_item(self, id_or_index: Union[str, int]) -> None:
        """Remove an item from the spine."""
        pass
```

## Document Components

### `PackageDocument`

Represents the OPF package document.

```python
from typing import List

class PackageDocument:
    @property
    def metadata(self) -> "EPUBMetadata":
        """Get the package metadata."""
        pass

    @property
    def manifest(self) -> "EPUBManifest":
        """Get the package manifest."""
        pass

    @property
    def spine(self) -> "EPUBSpine":
        """Get the package spine."""
        pass

    @property
    def collections(self) -> List["EPUBCollection"]:
        """Get the package collections."""
        pass

    # Parse and generate methods
    @staticmethod
    def parse(xml: str) -> "PackageDocument":
        """Parse an OPF document from XML."""
        pass

    def to_xml(self) -> str:
        """Convert the package document to XML."""
        pass
```

### `ContentDocument`

Base class for EPUB content documents.

```python
from abc import ABC, abstractmethod

class ContentDocument(ABC):
    @property
    def id(self) -> str:
        """Get the document ID."""
        pass

    @property
    def path(self) -> str:
        """Get the document path."""
        pass

    @property
    def media_type(self) -> str:
        """Get the document media type."""
        pass

    # Load and save content
    @abstractmethod
    def load(self) -> None:
        """Load the document content."""
        pass

    @abstractmethod
    def save(self) -> str:
        """Save the document content."""
        pass
```

### `XHTMLDocument`

Represents an XHTML content document.

```python
from typing import Optional, List

class XHTMLDocument(ContentDocument):
    @property
    def dom(self) -> Any:  # Any represents a DOM-like object
        """Get the document DOM."""
        pass

    @dom.setter
    def dom(self, value: Any) -> None:
        """Set the document DOM."""
        pass

    # Manipulation methods
    def query_selector(self, selector: str) -> Optional[Any]:
        """Find an element using a CSS selector."""
        pass

    def query_selector_all(self, selector: str) -> List[Any]:
        """Find all elements matching a CSS selector."""
        pass

    # EPUB-specific extensions
    def add_epub_type(self, element: Any, type: str) -> None:
        """Add an epub:type attribute to an element."""
        pass

    def get_elements_with_epub_type(self, type: str) -> List[Any]:
        """Get all elements with a specific epub:type."""
        pass
```

### `SVGDocument`

Represents an SVG content document.

```python
class SVGDocument(ContentDocument):
    @property
    def dom(self) -> Any:  # Any represents a DOM-like object
        """Get the document DOM."""
        pass

    @dom.setter
    def dom(self, value: Any) -> None:
        """Set the document DOM."""
        pass

    # SVG-specific methods
    def get_view_box(self) -> str:
        """Get the SVG viewBox attribute."""
        pass

    def set_view_box(self, value: str) -> None:
        """Set the SVG viewBox attribute."""
        pass
```

### `NavigationDocument`

Represents the EPUB navigation document.

```python
from typing import List

class NavigationDocument(XHTMLDocument):
    @property
    def toc(self) -> List["NavPoint"]:
        """Get the table of contents."""
        pass

    @property
    def page_list(self) -> List["NavPoint"]:
        """Get the page list."""
        pass

    @property
    def landmarks(self) -> List["NavPoint"]:
        """Get the landmarks."""
        pass

    # Methods
    def add_nav_point(self, nav_point: "NavPoint", type: str) -> None:
        """Add a navigation point to a specific nav type."""
        pass

    def remove_nav_point(self, id: str, type: str) -> None:
        """Remove a navigation point from a specific nav type."""
        pass
```

## Media and Layout

### `MediaOverlay`

Represents media overlay documents.

```python
from typing import List, Optional

class MediaOverlay:
    @property
    def id(self) -> str:
        """Get the media overlay ID."""
        pass

    @property
    def duration(self) -> float:
        """Get the total duration in seconds."""
        pass

    @property
    def narrators(self) -> List[str]:
        """Get the list of narrators."""
        pass

    # Media overlay operations
    def get_parallels(self) -> List["MediaOverlayParallel"]:
        """Get all parallel time containers."""
        pass

    def get_audio_for_text_element(self, text_path: str, element_id: str) -> Optional["AudioClip"]:
        """Get the audio clip for a specific text element."""
        pass

    # Creation methods
    def add_audio_clip(self, text_path: str, element_id: str, audio_src: str, begin: float, end: float) -> None:
        """Add an audio clip for a text element."""
        pass
```

### `LayoutManager`

Handles fixed and reflowable layouts.

```python
from typing import Literal

class LayoutManager:
    @property
    def is_fixed_layout(self) -> bool:
        """Check if this is a fixed layout publication."""
        pass

    @property
    def orientation(self) -> Literal["auto", "portrait", "landscape"]:
        """Get the orientation setting."""
        pass

    @property
    def spread_behavior(self) -> Literal["auto", "none", "landscape"]:
        """Get the spread behavior setting."""
        pass

    # Layout settings
    def set_fixed_layout(self, is_fixed: bool) -> None:
        """Set whether this is a fixed layout publication."""
        pass

    def set_orientation(self, orientation: Literal["auto", "portrait", "landscape"]) -> None:
        """Set the orientation setting."""
        pass

    def set_spread_behavior(self, behavior: Literal["auto", "none", "landscape"]) -> None:
        """Set the spread behavior setting."""
        pass
```

## Resources and Assets

### `Resource`

Represents any resource in the EPUB publication.

```python
class Resource:
    def __init__(self, id: str, path: str, media_type: str, data: bytes):
        self.id = id
        self.path = path
        self.media_type = media_type
        self._data = data

    @property
    def id(self) -> str:
        """Get the resource ID."""
        return self._id

    @property
    def path(self) -> str:
        """Get the resource path."""
        return self._path

    @property
    def media_type(self) -> str:
        """Get the resource media type."""
        return self._media_type

    # Resource handling
    def get_data(self) -> bytes:
        """Get the resource data as bytes."""
        return self._data

    def get_text(self) -> str:
        """Get the resource data as text."""
        return self._data.decode('utf-8')

    def set_data(self, data: Union[bytes, str]) -> None:
        """Set the resource data."""
        if isinstance(data, str):
            self._data = data.encode('utf-8')
        else:
            self._data = data
```

### `FontResource`

Specialized resource for font handling.

```python
class FontResource(Resource):
    @property
    def is_obfuscated(self) -> bool:
        """Check if the font is obfuscated."""
        pass

    # Font-specific operations
    def obfuscate(self) -> None:
        """Obfuscate the font according to the EPUB spec."""
        pass

    def deobfuscate(self) -> None:
        """Deobfuscate the font according to the EPUB spec."""
        pass
```

## Validation and Accessibility

### `Validator`

Handles EPUB validation.

```python
class Validator:
    def validate(self, epub: "EPUBContainer") -> "ValidationResult":
        """Validate the entire EPUB publication."""
        pass

    def validate_package(self, package_doc: "PackageDocument") -> "ValidationResult":
        """Validate just the package document."""
        pass

    def validate_navigation(self, nav_doc: "NavigationDocument") -> "ValidationResult":
        """Validate just the navigation document."""
        pass

    def validate_content(self, content_doc: "ContentDocument") -> "ValidationResult":
        """Validate a single content document."""
        pass
```

### `AccessibilityChecker`

Validates accessibility compliance.

```python
from typing import List

class AccessibilityChecker:
    def check(self, epub: "EPUBContainer") -> "AccessibilityReport":
        """Check the accessibility of the EPUB publication."""
        pass

    # Specific checks
    def check_metadata(self) -> List["AccessibilityIssue"]:
        """Check accessibility of metadata."""
        pass

    def check_content(self) -> List["AccessibilityIssue"]:
        """Check accessibility of content."""
        pass

    def check_navigation(self) -> List["AccessibilityIssue"]:
        """Check accessibility of navigation."""
        pass
```

## Helper Classes

### `EPUBMetadata`

```python
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EPUBMetadata:
    identifier: str
    title: str
    language: str
    creator: Optional[List[str]] = None
    contributor: Optional[List[str]] = None
    publisher: Optional[str] = None
    description: Optional[str] = None
    publication_date: Optional[datetime] = None
    modified: Optional[datetime] = None
    rights: Optional[str] = None
    # Additional extension metadata
    extra: Dict[str, Any] = None
```

### `ManifestItem`

```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class ManifestItem:
    id: str
    href: str
    media_type: str
    properties: Optional[List[str]] = None
    fallback: Optional[str] = None
    media_overlay: Optional[str] = None
```

### `EPUBManifest`

```python
from typing import List, Optional

class EPUBManifest:
    @property
    def items(self) -> List["ManifestItem"]:
        """Get all manifest items."""
        pass

    def get_item(self, id: str) -> Optional["ManifestItem"]:
        """Get a manifest item by ID."""
        pass

    def add_item(self, item: "ManifestItem") -> None:
        """Add an item to the manifest."""
        pass

    def remove_item(self, id: str) -> None:
        """Remove an item from the manifest."""
        pass
```

### `SpineItem`

```python
from dataclasses import dataclass
from typing import Optional, Literal

@dataclass
class SpineItem:
    idref: str
    linear: Literal["yes", "no"] = "yes"
    properties: Optional[List[str]] = None
    id: Optional[str] = None
```

### `EPUBSpine`

```python
from typing import List, Optional, Union

class EPUBSpine:
    @property
    def items(self) -> List["SpineItem"]:
        """Get all spine items."""
        pass

    @property
    def direction(self) -> Literal["ltr", "rtl"]:
        """Get the reading direction."""
        pass

    def get_item(self, idref: str) -> Optional["SpineItem"]:
        """Get a spine item by idref."""
        pass

    def add_item(self, item: "SpineItem", index: Optional[int] = None) -> None:
        """Add an item to the spine."""
        pass

    def remove_item(self, idref_or_index: Union[str, int]) -> None:
        """Remove an item from the spine."""
        pass
```

### `ValidationResult`

```python
from dataclasses import dataclass
from typing import List

@dataclass
class ValidationError:
    message: str
    location: str
    severity: str

@dataclass
class ValidationWarning:
    message: str
    location: str

@dataclass
class ValidationResult:
    valid: bool
    errors: List[ValidationError]
    warnings: List[ValidationWarning]
```

## Usage Examples

### Reading an EPUB

```python
# Create EPUB instance
epub_processor = EPUB()

# Read an EPUB file
epub = epub_processor.open('/path/to/book.epub')

# Access package metadata
print(f"Title: {epub.metadata.title}")
print(f"Author: {', '.join(epub.metadata.creator or [])}")

# Get table of contents
nav = epub.get_navigation()
print(f"Table of Contents: {nav.toc}")

# Read a content document
content_id = epub.spine.items[0].idref
content = epub.get_content_document(content_id)
```

### Creating an EPUB

```python
import uuid
from datetime import datetime

# Create EPUB instance
epub_processor = EPUB()

# Create a new EPUB
metadata = EPUBMetadata(
    identifier=f"urn:uuid:{uuid.uuid4()}",
    title="My New Book",
    language="en",
    creator=["Author Name"],
    modified=datetime.now()
)
epub = epub_processor.create(metadata)

# Add a stylesheet
css = Resource(
    id="style",
    path="styles/main.css",
    media_type="text/css",
    data=b"body { font-family: serif; }"
)
epub.add_resource(css)

# Add a chapter
from lxml import etree
html = etree.fromstring('<html><body><h1>Chapter 1</h1><p>Content here</p></body></html>'.encode('utf-8'))
chapter = XHTMLDocument(id="chapter1", path="text/chapter1.xhtml", media_type="application/xhtml+xml")
chapter.dom = html
epub.add_resource(chapter)

# Update spine
epub.add_spine_item(SpineItem(idref="chapter1", linear="yes"))

# Write the EPUB
epub_processor.write(epub, '/path/to/output.epub')
```
