"""Container model for EPUB3 publications."""

from typing import Any, Dict, Optional, Union


from epub3.models.content_document import ContentDocument, SVGDocument, XHTMLDocument
from epub3.models.manifest import EPUBManifest, ManifestItem
from epub3.models.metadata import EPUBMetadata
from epub3.models.navigation_document import NavigationDocument
from epub3.models.package_document import PackageDocument
from epub3.models.resource import Resource
from epub3.models.spine import EPUBSpine, SpineItem


class EPUBContainer:
    """Represents an EPUB publication with all its components.

    Attributes:
        _resources: Dictionary of resources in the container
        _package_document: The package document
        _content_documents: Dictionary of content documents
        _navigation_document: The navigation document
    """

    def __init__(self, package_document: PackageDocument):
        """Initialize an EPUB container.

        Args:
            package_document: The package document
        """
        self._resources: Dict[str, Resource] = {}
        self._package_document = package_document
        self._content_documents: Dict[str, ContentDocument] = {}
        self._navigation_document: Optional[NavigationDocument] = None

    @property
    def metadata(self) -> EPUBMetadata:
        """Get the EPUB metadata.

        Returns:
            The EPUB metadata
        """
        return self._package_document.metadata

    @property
    def manifest(self) -> EPUBManifest:
        """Get the EPUB manifest.

        Returns:
            The EPUB manifest
        """
        return self._package_document.manifest

    @property
    def spine(self) -> EPUBSpine:
        """Get the EPUB spine.

        Returns:
            The EPUB spine
        """
        return self._package_document.spine

    @property
    def navigation(self) -> Optional[NavigationDocument]:
        """Get the EPUB navigation.

        Returns:
            The EPUB navigation document, or None if not set
        """
        return self._navigation_document

    def get_package_document(self) -> PackageDocument:
        """Get the package document.

        Returns:
            The package document
        """
        return self._package_document

    def get_content_document(self, id: str) -> Optional[ContentDocument]:
        """Get a content document by ID.

        Args:
            id: The ID of the content document

        Returns:
            The content document, or None if not found
        """
        return self._content_documents.get(id)

    def get_navigation(self) -> Optional[NavigationDocument]:
        """Get the navigation document.

        Returns:
            The navigation document, or None if not set
        """
        return self._navigation_document

    def get_resource(self, path: str) -> Optional[Resource]:
        """Get a resource by path.

        Args:
            path: The path to the resource

        Returns:
            The resource, or None if not found
        """
        # Normalize the path for comparison
        normalized_path = path.replace("\\", "/")

        # Try to get the resource directly
        if normalized_path in self._resources:
            return self._resources[normalized_path]

        # If not found, try case-insensitive comparison
        for res_path, resource in self._resources.items():
            if res_path.lower() == normalized_path.lower():
                return resource

        return None

    def add_resource(self, resource: Resource) -> None:
        """Add a resource to the EPUB.

        Args:
            resource: The resource to add

        Raises:
            ValueError: If a resource with the same path already exists
        """
        # Normalize the path for storage
        normalized_path = resource.path.replace("\\", "/")

        if normalized_path in self._resources:
            raise ValueError(f"Resource with path '{normalized_path}' already exists")

        self._resources[normalized_path] = resource

        # If this resource is referenced in the manifest, we need to make sure
        # it can be added as a content document if appropriate
        manifest_item = self._get_manifest_item_by_href(normalized_path)
        if manifest_item:
            self._process_manifest_item(manifest_item)

    def remove_resource(self, path: str) -> None:
        """Remove a resource from the EPUB.

        Args:
            path: The path to the resource

        Raises:
            KeyError: If the resource is not found
        """
        # Normalize the path for lookup
        normalized_path = path.replace("\\", "/")

        if normalized_path not in self._resources:
            raise KeyError(f"Resource with path '{normalized_path}' not found")

        # Remove from resources
        del self._resources[normalized_path]

        # Check if this was a content document and remove it if so
        for id_value, content_doc in list(self._content_documents.items()):
            if content_doc.path == normalized_path:
                del self._content_documents[id_value]
                break

        # Check if this was the navigation document
        if (
            self._navigation_document
            and self._navigation_document.path == normalized_path
        ):
            self._navigation_document = None

    def update_metadata(self, metadata: Union[EPUBMetadata, Dict[str, Any]]) -> None:
        """Update the EPUB metadata.

        Args:
            metadata: The new metadata, either as an EPUBMetadata object or a dictionary
        """
        if isinstance(metadata, dict):
            # Create a new metadata object with updated values
            current = self._package_document.metadata

            # Copy existing values
            new_metadata = EPUBMetadata(
                identifier=metadata.get("identifier", current.identifier),
                title=metadata.get("title", current.title),
                language=metadata.get("language", current.language),
                creator=metadata.get("creator", current.creator),
                contributor=metadata.get("contributor", current.contributor),
                publisher=metadata.get("publisher", current.publisher),
                description=metadata.get("description", current.description),
                publication_date=metadata.get(
                    "publication_date", current.publication_date
                ),
                modified=metadata.get("modified", current.modified),
                rights=metadata.get("rights", current.rights),
            )

            # Copy extra metadata
            new_metadata.extra = current.extra.copy()
            if "extra" in metadata:
                new_metadata.extra.update(metadata["extra"])

            # Update the package document
            self._package_document._metadata = new_metadata
        else:
            # Use the provided metadata object directly
            self._package_document._metadata = metadata

    def add_spine_item(self, item: SpineItem, index: Optional[int] = None) -> None:
        """Add an item to the spine.

        Args:
            item: The spine item to add
            index: Optional position to insert the item at

        Raises:
            ValueError: If the referenced manifest item doesn't exist
        """
        # Check if the referenced manifest item exists
        if not self._package_document.manifest.get_item(item.idref):
            raise ValueError(f"Manifest item with ID '{item.idref}' not found")

        # Add to the spine
        self._package_document.spine.add_item(item, index)

    def remove_spine_item(self, id_or_index: Union[str, int]) -> None:
        """Remove an item from the spine.

        Args:
            id_or_index: Either the idref of the item or its index

        Raises:
            KeyError: If the item doesn't exist (when using idref)
            IndexError: If the index is out of range
        """
        self._package_document.spine.remove_item(id_or_index)

    def set_navigation_document(self, nav_doc: NavigationDocument) -> None:
        """Set the navigation document.

        Args:
            nav_doc: The navigation document
        """
        self._navigation_document = nav_doc

        # Add it as a content document if it's not already there
        if nav_doc.id not in self._content_documents:
            self._content_documents[nav_doc.id] = nav_doc

    def _get_manifest_item_by_href(self, href: str) -> Optional[ManifestItem]:
        """Get a manifest item by href.

        Args:
            href: The href to look for

        Returns:
            The manifest item, or None if not found
        """
        # Normalize the href for comparison
        normalized_href = href.replace("\\", "/")

        for item in self._package_document.manifest.items:
            if item.href.replace("\\", "/") == normalized_href:
                return item

        return None

    def _process_manifest_item(self, item: ManifestItem) -> None:
        """Process a manifest item, creating the appropriate content document.

        Args:
            item: The manifest item to process
        """
        # Check if we have a resource for this item
        resource = self.get_resource(item.href)
        if not resource:
            return

        # Create the appropriate content document based on media type
        if item.media_type == "application/xhtml+xml":
            # Check if this is a navigation document
            is_nav = item.properties and "nav" in item.properties

            if is_nav:
                nav_doc = NavigationDocument(item.id, item.href)
                nav_doc.load(resource.get_data())
                self._navigation_document = nav_doc
                self._content_documents[item.id] = nav_doc
            else:
                content_doc = XHTMLDocument(item.id, item.href)
                content_doc.load(resource.get_data())
                self._content_documents[item.id] = content_doc

        elif item.media_type == "image/svg+xml":
            content_doc = SVGDocument(item.id, item.href)
            content_doc.load(resource.get_data())
            self._content_documents[item.id] = content_doc
