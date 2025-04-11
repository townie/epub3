"""Content document models for EPUB3 publications."""

from abc import ABC, abstractmethod
from typing import List, Optional

from lxml import etree


class ContentDocument(ABC):
    """Base class for EPUB content documents.

    Attributes:
        _id: The document ID
        _path: The document path within the EPUB container
        _media_type: The document media type
        _content: The document content as bytes
    """

    def __init__(self, id: str, path: str, media_type: str):
        """Initialize a content document.

        Args:
            id: The document ID
            path: The document path within the EPUB container
            media_type: The document media type
        """
        self._id = id
        self._path = path
        self._media_type = media_type
        self._content: Optional[bytes] = None

    @property
    def id(self) -> str:
        """Get the document ID.

        Returns:
            The document ID
        """
        return self._id

    @property
    def path(self) -> str:
        """Get the document path.

        Returns:
            The document path within the EPUB container
        """
        return self._path

    @property
    def media_type(self) -> str:
        """Get the document media type.

        Returns:
            The document media type
        """
        return self._media_type

    @abstractmethod
    def load(self, content: bytes) -> None:
        """Load the document content.

        Args:
            content: The document content as bytes
        """

    @abstractmethod
    def save(self) -> bytes:
        """Save the document content.

        Returns:
            The document content as bytes
        """


class XHTMLDocument(ContentDocument):
    """Represents an XHTML content document.

    Attributes:
        _dom: The document DOM
    """

    def __init__(self, id: str, path: str, media_type: str = "application/xhtml+xml"):
        """Initialize an XHTML document.

        Args:
            id: The document ID
            path: The document path within the EPUB container
            media_type: The document media type, defaults to application/xhtml+xml
        """
        super().__init__(id, path, media_type)
        self._dom: Optional[etree._ElementTree] = None

    @property
    def dom(self) -> Optional[etree._ElementTree]:
        """Get the document DOM.

        Returns:
            The document DOM
        """
        return self._dom

    @dom.setter
    def dom(self, value: etree._ElementTree) -> None:
        """Set the document DOM.

        Args:
            value: The document DOM
        """
        self._dom = value

    def load(self, content: bytes) -> None:
        """Load the document content.

        Args:
            content: The document content as bytes
        """
        self._content = content
        parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
        self._dom = etree.fromstring(content, parser=parser)
        if not isinstance(self._dom, etree._Element):
            raise ValueError("Failed to parse XHTML content")
        # Convert to ElementTree
        self._dom = etree.ElementTree(self._dom)

    def save(self) -> bytes:
        """Save the document content.

        Returns:
            The document content as bytes

        Raises:
            ValueError: If the DOM is not set
        """
        if self._dom is None:
            raise ValueError("Document DOM is not set")
        return etree.tostring(
            self._dom, encoding="utf-8", xml_declaration=True, pretty_print=True
        )

    def query_selector(self, selector: str) -> Optional[etree._Element]:
        """Find an element using a CSS selector.

        Args:
            selector: The CSS selector

        Returns:
            The first matching element, or None if not found

        Raises:
            ValueError: If the DOM is not set
        """
        if self._dom is None:
            raise ValueError("Document DOM is not set")

        # This is a simplified implementation that handles only simple cases
        # A real implementation would use a CSS selector engine like cssselect
        if selector.startswith("#"):
            # ID selector
            element_id = selector[1:]
            xpath = f".//*[@id='{element_id}']"
        elif selector.startswith("."):
            # Class selector
            class_name = selector[1:]
            xpath = f".//*[contains(@class,'{class_name}')]"
        else:
            # Element selector
            xpath = f".//{selector}"

        results = self._dom.xpath(xpath)
        return results[0] if results else None

    def query_selector_all(self, selector: str) -> List[etree._Element]:
        """Find all elements matching a CSS selector.

        Args:
            selector: The CSS selector

        Returns:
            List of matching elements

        Raises:
            ValueError: If the DOM is not set
        """
        if self._dom is None:
            raise ValueError("Document DOM is not set")

        # This is a simplified implementation that handles only simple cases
        if selector.startswith("#"):
            # ID selector
            element_id = selector[1:]
            xpath = f".//*[@id='{element_id}']"
        elif selector.startswith("."):
            # Class selector
            class_name = selector[1:]
            xpath = f".//*[contains(@class,'{class_name}')]"
        else:
            # Element selector
            xpath = f".//{selector}"

        return self._dom.xpath(xpath)

    def add_epub_type(self, element: etree._Element, type_value: str) -> None:
        """Add an epub:type attribute to an element.

        Args:
            element: The element to modify
            type_value: The value for the epub:type attribute

        Raises:
            ValueError: If the element is not part of this document
        """
        if self._dom is None:
            raise ValueError("Document DOM is not set")

        # Check if the element belongs to this document
        if element.getroottree() is not self._dom:
            raise ValueError("Element does not belong to this document")

        # Add or update the epub:type attribute
        ns = "http://www.idpf.org/2007/ops"
        etree.register_namespace("epub", ns)
        element.attrib[f"{{{ns}}}type"] = type_value

    def get_elements_with_epub_type(self, type_value: str) -> List[etree._Element]:
        """Get all elements with a specific epub:type.

        Args:
            type_value: The epub:type value to search for

        Returns:
            List of matching elements

        Raises:
            ValueError: If the DOM is not set
        """
        if self._dom is None:
            raise ValueError("Document DOM is not set")

        ns = "http://www.idpf.org/2007/ops"
        return self._dom.xpath(
            f".//*[@epub:type='{type_value}']", namespaces={"epub": ns}
        )


class SVGDocument(ContentDocument):
    """Represents an SVG content document.

    Attributes:
        _dom: The document DOM
    """

    def __init__(self, id: str, path: str, media_type: str = "image/svg+xml"):
        """Initialize an SVG document.

        Args:
            id: The document ID
            path: The document path within the EPUB container
            media_type: The document media type, defaults to image/svg+xml
        """
        super().__init__(id, path, media_type)
        self._dom: Optional[etree._ElementTree] = None

    @property
    def dom(self) -> Optional[etree._ElementTree]:
        """Get the document DOM.

        Returns:
            The document DOM
        """
        return self._dom

    @dom.setter
    def dom(self, value: etree._ElementTree) -> None:
        """Set the document DOM.

        Args:
            value: The document DOM
        """
        self._dom = value

    def load(self, content: bytes) -> None:
        """Load the document content.

        Args:
            content: The document content as bytes
        """
        self._content = content
        parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
        self._dom = etree.fromstring(content, parser=parser)
        if not isinstance(self._dom, etree._Element):
            raise ValueError("Failed to parse SVG content")
        # Convert to ElementTree
        self._dom = etree.ElementTree(self._dom)

    def save(self) -> bytes:
        """Save the document content.

        Returns:
            The document content as bytes

        Raises:
            ValueError: If the DOM is not set
        """
        if self._dom is None:
            raise ValueError("Document DOM is not set")
        return etree.tostring(
            self._dom, encoding="utf-8", xml_declaration=True, pretty_print=True
        )

    def get_view_box(self) -> Optional[str]:
        """Get the SVG viewBox attribute.

        Returns:
            The viewBox attribute value, or None if not set

        Raises:
            ValueError: If the DOM is not set
        """
        if self._dom is None or self._dom.getroot() is None:
            raise ValueError("Document DOM is not set")

        return self._dom.getroot().get("viewBox")

    def set_view_box(self, value: str) -> None:
        """Set the SVG viewBox attribute.

        Args:
            value: The viewBox attribute value

        Raises:
            ValueError: If the DOM is not set
        """
        if self._dom is None or self._dom.getroot() is None:
            raise ValueError("Document DOM is not set")

        self._dom.getroot().set("viewBox", value)
