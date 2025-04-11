"""Spine model for EPUB3 publications."""

from dataclasses import dataclass
from typing import List, Literal, Optional, Union


@dataclass
class SpineItem:
    """Represents an item in the EPUB spine.

    Attributes:
        idref: Reference to a manifest item ID
        linear: Whether the item is part of the linear reading order
        properties: Optional list of properties
        id: Optional unique identifier for the spine item itself
    """

    idref: str
    linear: Literal["yes", "no"] = "yes"
    properties: Optional[List[str]] = None
    id: Optional[str] = None


class EPUBSpine:
    """Represents the spine section of an EPUB package document.

    The spine defines the reading order of the EPUB publication.

    Attributes:
        _items: List of spine items in reading order
        _direction: Reading direction (ltr or rtl)
    """

    def __init__(self, direction: Literal["ltr", "rtl"] = "ltr"):
        """Initialize an empty spine.

        Args:
            direction: Reading direction, either "ltr" (left-to-right) or
                "rtl" (right-to-left)
        """
        self._items: List[SpineItem] = []
        self._direction: Literal["ltr", "rtl"] = direction

    @property
    def items(self) -> List[SpineItem]:
        """Get all spine items.

        Returns:
            List of all spine items in reading order
        """
        return self._items.copy()

    @property
    def direction(self) -> Literal["ltr", "rtl"]:
        """Get the reading direction.

        Returns:
            The reading direction, either "ltr" or "rtl"
        """
        return self._direction

    @direction.setter
    def direction(self, value: Literal["ltr", "rtl"]) -> None:
        """Set the reading direction.

        Args:
            value: The reading direction, either "ltr" or "rtl"

        Raises:
            ValueError: If the value is not "ltr" or "rtl"
        """
        if value not in ["ltr", "rtl"]:
            raise ValueError("Direction must be either 'ltr' or 'rtl'")
        self._direction = value

    def get_item(self, idref: str) -> Optional[SpineItem]:
        """Get a spine item by idref.

        Args:
            idref: The reference to a manifest item ID

        Returns:
            The spine item, or None if not found
        """
        for item in self._items:
            if item.idref == idref:
                return item
        return None

    def add_item(self, item: SpineItem, index: Optional[int] = None) -> None:
        """Add an item to the spine.

        Args:
            item: The spine item to add
            index: Optional position to insert the item at. If None, append to the end.

        Raises:
            ValueError: If an item with the same idref already exists
            IndexError: If the index is out of range
        """
        if self.get_item(item.idref):
            raise ValueError(f"Spine item with idref '{item.idref}' already exists")

        if index is None:
            self._items.append(item)
        else:
            if index < 0 or (self._items and index > len(self._items)):
                raise IndexError("Spine index out of range")
            self._items.insert(index, item)

    def remove_item(self, idref_or_index: Union[str, int]) -> None:
        """Remove an item from the spine.

        Args:
            idref_or_index: Either the idref of the item or its index

        Raises:
            KeyError: If the item doesn't exist (when using idref)
            IndexError: If the index is out of range
        """
        if isinstance(idref_or_index, str):
            # Remove by idref
            for i, item in enumerate(self._items):
                if item.idref == idref_or_index:
                    del self._items[i]
                    return
            raise KeyError(f"Spine item with idref '{idref_or_index}' not found")
        else:
            # Remove by index
            if idref_or_index < 0 or idref_or_index >= len(self._items):
                raise IndexError("Spine index out of range")
            del self._items[idref_or_index]
