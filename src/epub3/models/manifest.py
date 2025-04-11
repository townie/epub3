"""Manifest model for EPUB3 publications."""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ManifestItem:
    """Represents an item in the EPUB manifest.

    Attributes:
        id: The identifier of the item
        href: The path to the item
        media_type: The MIME type of the item
        properties: Optional list of properties
        fallback: Optional ID of a fallback item
        media_overlay: Optional ID of a media overlay document
    """

    id: str
    href: str
    media_type: str
    properties: Optional[List[str]] = None
    fallback: Optional[str] = None
    media_overlay: Optional[str] = None


class EPUBManifest:
    """Represents the manifest section of an EPUB package document.

    The manifest contains a list of all the items in the EPUB publication.

    Attributes:
        _items: Dictionary of manifest items, keyed by ID
    """

    def __init__(self):
        """Initialize an empty manifest."""
        self._items: Dict[str, ManifestItem] = {}

    @property
    def items(self) -> List[ManifestItem]:
        """Get all manifest items.

        Returns:
            List of all manifest items
        """
        return list(self._items.values())

    def get_item(self, id: str) -> Optional[ManifestItem]:
        """Get a manifest item by ID.

        Args:
            id: The ID of the manifest item

        Returns:
            The manifest item, or None if not found
        """
        return self._items.get(id)

    def add_item(self, item: ManifestItem) -> None:
        """Add an item to the manifest.

        Args:
            item: The manifest item to add

        Raises:
            ValueError: If an item with the same ID already exists
        """
        if item.id in self._items:
            raise ValueError(f"Manifest item with ID '{item.id}' already exists")
        self._items[item.id] = item

    def remove_item(self, id: str) -> None:
        """Remove an item from the manifest.

        Args:
            id: The ID of the manifest item to remove

        Raises:
            KeyError: If the item doesn't exist
        """
        if id not in self._items:
            raise KeyError(f"Manifest item with ID '{id}' not found")
        del self._items[id]

    def has_item(self, id: str) -> bool:
        """Check if an item with the given ID exists.

        Args:
            id: The ID to check

        Returns:
            True if the item exists, False otherwise
        """
        return id in self._items
