"""Navigation document models for EPUB3 publications."""

from dataclasses import dataclass, field
from typing import List, Literal, Optional

from lxml import etree

from epub3.models.content_document import XHTMLDocument


@dataclass
class NavPoint:
    """Represents a navigation point within a navigation document.

    Attributes:
        text: The text of the navigation point
        href: The target URL
        id: Optional identifier for the navigation point
        children: Optional list of child navigation points
    """

    text: str
    href: str
    id: Optional[str] = None
    children: List["NavPoint"] = field(default_factory=list)


class NavigationDocument(XHTMLDocument):
    """Represents the EPUB navigation document.

    The navigation document contains the table of contents, page list, and landmarks.

    Attributes:
        _toc: The table of contents
        _page_list: The page list
        _landmarks: The landmarks
    """

    def __init__(self, id: str, path: str):
        """Initialize a navigation document.

        Args:
            id: The document ID
            path: The document path within the EPUB container
        """
        super().__init__(id, path)
        self._toc: List[NavPoint] = []
        self._page_list: List[NavPoint] = []
        self._landmarks: List[NavPoint] = []

    @property
    def toc(self) -> List[NavPoint]:
        """Get the table of contents.

        Returns:
            The table of contents as a list of NavPoints
        """
        return self._toc.copy()

    @property
    def page_list(self) -> List[NavPoint]:
        """Get the page list.

        Returns:
            The page list as a list of NavPoints
        """
        return self._page_list.copy()

    @property
    def landmarks(self) -> List[NavPoint]:
        """Get the landmarks.

        Returns:
            The landmarks as a list of NavPoints
        """
        return self._landmarks.copy()

    def add_nav_point(
        self, nav_point: NavPoint, type_value: Literal["toc", "page-list", "landmarks"]
    ) -> None:
        """Add a navigation point to a specific nav type.

        Args:
            nav_point: The navigation point to add
            type_value: The type of navigation ("toc", "page-list", or "landmarks")

        Raises:
            ValueError: If the type is not valid
        """
        if type_value == "toc":
            self._toc.append(nav_point)
        elif type_value == "page-list":
            self._page_list.append(nav_point)
        elif type_value == "landmarks":
            self._landmarks.append(nav_point)
        else:
            raise ValueError(f"Invalid navigation type: {type_value}")

    def remove_nav_point(
        self, id_value: str, type_value: Literal["toc", "page-list", "landmarks"]
    ) -> None:
        """Remove a navigation point from a specific nav type.

        Args:
            id_value: The ID of the navigation point to remove
            type_value: The type of navigation ("toc", "page-list", or "landmarks")

        Raises:
            ValueError: If the type is not valid
            KeyError: If the navigation point is not found
        """
        nav_list = None
        if type_value == "toc":
            nav_list = self._toc
        elif type_value == "page-list":
            nav_list = self._page_list
        elif type_value == "landmarks":
            nav_list = self._landmarks
        else:
            raise ValueError(f"Invalid navigation type: {type_value}")

        def remove_by_id(nav_points: List[NavPoint]) -> bool:
            for i, nav_point in enumerate(nav_points):
                if nav_point.id == id_value:
                    del nav_points[i]
                    return True
                if remove_by_id(nav_point.children):
                    return True
            return False

        if not remove_by_id(nav_list):
            raise KeyError(
                f"Navigation point with ID '{id_value}' not found in {type_value}"
            )

    def load(self, content: bytes) -> None:
        """Load the document content and parse the navigation.

        Args:
            content: The document content as bytes
        """
        super().load(content)
        self._parse_navigation()

    def _parse_navigation(self) -> None:
        """Parse the navigation from the loaded DOM."""
        if self._dom is None:
            raise ValueError("Document DOM is not set")

        # Clear existing navigation
        self._toc = []
        self._page_list = []
        self._landmarks = []

        # Parse each navigation section
        self._parse_nav_section("toc")
        self._parse_nav_section("page-list")
        self._parse_nav_section("landmarks")

    def _parse_nav_section(self, type_value: str) -> None:
        """Parse a specific navigation section.

        Args:
            type_value: The type of navigation ("toc", "page-list", or "landmarks")
        """
        if self._dom is None:
            return

        # Find the nav element for this type
        ns = "http://www.idpf.org/2007/ops"
        nav_elements = self._dom.xpath(
            f"//nav[@epub:type='{type_value}']", namespaces={"epub": ns}
        )

        if not nav_elements:
            return

        nav_element = nav_elements[0]

        # Find the ol element that contains the list items
        ol_elements = nav_element.xpath(".//ol")
        if not ol_elements:
            return

        # Parse the list items recursively
        nav_points = self._parse_nav_list(ol_elements[0])

        # Store the parsed navigation points in the appropriate list
        if type_value == "toc":
            self._toc = nav_points
        elif type_value == "page-list":
            self._page_list = nav_points
        elif type_value == "landmarks":
            self._landmarks = nav_points

    def _parse_nav_list(self, ol_element: etree._Element) -> List[NavPoint]:
        """Parse a list of navigation points from an ol element.

        Args:
            ol_element: The ol element containing the navigation points

        Returns:
            List of parsed navigation points
        """
        nav_points = []

        for li_element in ol_element.xpath("./li"):
            # Get the link element (a)
            a_elements = li_element.xpath("./a")
            if not a_elements:
                # Skip this item if it doesn't have a link
                continue

            a_element = a_elements[0]

            # Get the text and href
            text = "".join(a_element.xpath(".//text()"))
            href = a_element.get("href", "")
            id_value = a_element.get("id")

            # Create a NavPoint
            nav_point = NavPoint(text=text, href=href, id=id_value)

            # Check for nested ol elements (children)
            nested_ol_elements = li_element.xpath("./ol")
            if nested_ol_elements:
                nav_point.children = self._parse_nav_list(nested_ol_elements[0])

            nav_points.append(nav_point)

        return nav_points

    def save(self) -> bytes:
        """Save the document content after updating the navigation.

        Returns:
            The document content as bytes
        """
        if self._dom is None:
            raise ValueError("Document DOM is not set")

        # Update the navigation sections in the DOM
        self._update_nav_section("toc", self._toc)
        self._update_nav_section("page-list", self._page_list)
        self._update_nav_section("landmarks", self._landmarks)

        return super().save()

    def _update_nav_section(self, type_value: str, nav_points: List[NavPoint]) -> None:
        """Update a specific navigation section in the DOM.

        Args:
            type_value: The type of navigation ("toc", "page-list", or "landmarks")
            nav_points: The navigation points to use
        """
        if self._dom is None:
            return

        # Find the nav element for this type
        ns = "http://www.idpf.org/2007/ops"
        nav_elements = self._dom.xpath(
            f"//nav[@epub:type='{type_value}']", namespaces={"epub": ns}
        )

        nav_element = None
        if nav_elements:
            # Use existing nav element
            nav_element = nav_elements[0]

            # Clear existing content
            ol_elements = nav_element.xpath(".//ol")
            for ol_element in ol_elements:
                ol_element.getparent().remove(ol_element)
        elif nav_points:
            # Create new nav element if there are nav points
            nav_element = etree.Element("nav")
            self.add_epub_type(nav_element, type_value)

            # Add a title
            title = etree.SubElement(nav_element, "h2")
            if type_value == "toc":
                title.text = "Table of Contents"
            elif type_value == "page-list":
                title.text = "List of Pages"
            elif type_value == "landmarks":
                title.text = "Landmarks"

            # Add to the body
            body = self._dom.xpath("//body")
            if body:
                body[0].append(nav_element)

        # If there are no nav points and no existing nav element, do nothing
        if not nav_element or not nav_points:
            return

        # Create a new ol element with the nav points
        ol_element = etree.SubElement(nav_element, "ol")
        self._create_nav_list(ol_element, nav_points)

    def _create_nav_list(
        self, ol_element: etree._Element, nav_points: List[NavPoint]
    ) -> None:
        """Create a list of navigation points in an ol element.

        Args:
            ol_element: The ol element to add navigation points to
            nav_points: The navigation points to add
        """
        for nav_point in nav_points:
            # Create li element
            li_element = etree.SubElement(ol_element, "li")

            # Create a element
            a_element = etree.SubElement(li_element, "a")
            a_element.text = nav_point.text
            a_element.set("href", nav_point.href)

            if nav_point.id:
                a_element.set("id", nav_point.id)

            # Add children if any
            if nav_point.children:
                nested_ol = etree.SubElement(li_element, "ol")
                self._create_nav_list(nested_ol, nav_point.children)
