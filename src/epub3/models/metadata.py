"""Metadata model for EPUB3 publications."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class EPUBMetadata:
    """Represents EPUB publication metadata.

    This class holds Dublin Core and other metadata elements for an EPUB publication.

    Attributes:
        identifier: The identifier of the publication (required)
        title: The title of the publication (required)
        language: The language of the publication (required)
        creator: List of creators/authors
        contributor: List of contributors
        publisher: The publisher of the publication
        description: A description of the publication
        publication_date: The publication date
        modified: The last modification date
        rights: Rights information for the publication
        extra: Additional metadata not covered by other fields
    """

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
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize and validate metadata fields."""
        if not self.identifier:
            raise ValueError("Identifier is required")
        if not self.title:
            raise ValueError("Title is required")
        if not self.language:
            raise ValueError("Language is required")
