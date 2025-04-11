"""Package document model for EPUB3 publications."""

from datetime import datetime
from typing import Dict, List, Optional

from lxml import etree

from epub3.models.manifest import EPUBManifest, ManifestItem
from epub3.models.metadata import EPUBMetadata
from epub3.models.spine import EPUBSpine, SpineItem


class EPUBCollection:
    """Represents a collection in an EPUB package document.

    Attributes:
        _role: The role of the collection
        _items: The items in the collection
    """

    def __init__(self, role: str):
        """Initialize an EPUB collection.

        Args:
            role: The role of the collection
        """
        self._role = role
        self._items: List[str] = []

    @property
    def role(self) -> str:
        """Get the role of the collection.

        Returns:
            The role of the collection
        """
        return self._role

    @property
    def items(self) -> List[str]:
        """Get the items in the collection.

        Returns:
            The items in the collection
        """
        return self._items.copy()

    def add_item(self, item: str) -> None:
        """Add an item to the collection.

        Args:
            item: The item to add
        """
        if item not in self._items:
            self._items.append(item)

    def remove_item(self, item: str) -> None:
        """Remove an item from the collection.

        Args:
            item: The item to remove

        Raises:
            ValueError: If the item is not in the collection
        """
        if item not in self._items:
            raise ValueError(f"Item '{item}' not in collection")
        self._items.remove(item)


class PackageDocument:
    """Represents the OPF package document.

    Attributes:
        _metadata: The package metadata
        _manifest: The package manifest
        _spine: The package spine
        _collections: The package collections
        _unique_identifier: The unique identifier of the publication
        _version: The EPUB version
        _direction: The reading direction (ltr or rtl)
        _xml: The XML document
        _xmlns: The XML namespace declarations
    """

    def __init__(self, metadata: Optional[EPUBMetadata] = None):
        """Initialize an empty package document.

        Args:
            metadata: Optional metadata to initialize with
        """
        if metadata:
            self._metadata = metadata
        else:
            # Create a placeholder metadata with valid defaults
            self._metadata = EPUBMetadata(
                identifier="urn:uuid:placeholder", title="Untitled", language="en"
            )

        self._manifest = EPUBManifest()
        self._spine = EPUBSpine()
        self._collections: List[EPUBCollection] = []
        self._unique_identifier = "pub-id"
        self._version = "3.0"
        self._direction = "default"
        self._xml: Optional[etree._ElementTree] = None
        self._xmlns: Dict[str, str] = {
            None: "http://www.idpf.org/2007/opf",
            "dc": "http://purl.org/dc/elements/1.1/",
            "epub": "http://www.idpf.org/2007/ops",
        }

    @property
    def metadata(self) -> EPUBMetadata:
        """Get the package metadata.

        Returns:
            The package metadata
        """
        return self._metadata

    @property
    def manifest(self) -> EPUBManifest:
        """Get the package manifest.

        Returns:
            The package manifest
        """
        return self._manifest

    @property
    def spine(self) -> EPUBSpine:
        """Get the package spine.

        Returns:
            The package spine
        """
        return self._spine

    @property
    def collections(self) -> List[EPUBCollection]:
        """Get the package collections.

        Returns:
            The package collections
        """
        return self._collections.copy()

    @property
    def version(self) -> str:
        """Get the EPUB version.

        Returns:
            The EPUB version
        """
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        """Set the EPUB version.

        Args:
            value: The EPUB version
        """
        self._version = value

    @property
    def unique_identifier(self) -> str:
        """Get the unique identifier.

        Returns:
            The unique identifier
        """
        return self._unique_identifier

    @unique_identifier.setter
    def unique_identifier(self, value: str) -> None:
        """Set the unique identifier.

        Args:
            value: The unique identifier
        """
        self._unique_identifier = value

    @property
    def direction(self) -> str:
        """Get the reading direction.

        Returns:
            The reading direction
        """
        return self._direction

    @direction.setter
    def direction(self, value: str) -> None:
        """Set the reading direction.

        Args:
            value: The reading direction
        """
        self._direction = value

    def add_collection(self, collection: EPUBCollection) -> None:
        """Add a collection to the package.

        Args:
            collection: The collection to add

        Raises:
            ValueError: If a collection with the same role already exists
        """
        for existing in self._collections:
            if existing.role == collection.role:
                raise ValueError(
                    f"Collection with role '{collection.role}' already exists"
                )
        self._collections.append(collection)

    def get_collection(self, role: str) -> Optional[EPUBCollection]:
        """Get a collection by role.

        Args:
            role: The role of the collection

        Returns:
            The collection, or None if not found
        """
        for collection in self._collections:
            if collection.role == role:
                return collection
        return None

    def remove_collection(self, role: str) -> None:
        """Remove a collection from the package.

        Args:
            role: The role of the collection

        Raises:
            ValueError: If the collection is not found
        """
        for i, collection in enumerate(self._collections):
            if collection.role == role:
                del self._collections[i]
                return
        raise ValueError(f"Collection with role '{role}' not found")

    @staticmethod
    def parse(xml: str) -> "PackageDocument":
        """Parse an OPF document from XML.

        Args:
            xml: The XML string

        Returns:
            The parsed package document

        Raises:
            ValueError: If the XML is invalid
        """
        package_doc = PackageDocument()
        parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)

        try:
            root = etree.fromstring(xml.encode("utf-8"), parser=parser)
            if not isinstance(root, etree._Element):
                raise ValueError("Failed to parse OPF document")

            # Create ElementTree from root
            tree = etree.ElementTree(root)
            package_doc._xml = tree

            # Extract version and unique-identifier
            package_doc._version = root.get("version", "3.0")
            package_doc._unique_identifier = root.get("unique-identifier", "pub-id")
            package_doc._direction = root.get("dir", "default")

            # Parse metadata
            package_doc._parse_metadata(root)

            # Parse manifest
            package_doc._parse_manifest(root)

            # Parse spine
            package_doc._parse_spine(root)

            # Parse collections
            package_doc._parse_collections(root)

            return package_doc

        except Exception as e:
            raise ValueError(f"Error parsing OPF document: {str(e)}")

    def _parse_metadata(self, root: etree._Element) -> None:
        """Parse metadata from the package document.

        Args:
            root: The root element of the package document
        """
        # Find the metadata element
        metadata_elements = root.xpath("//*[local-name()='metadata']")
        if not metadata_elements:
            return

        metadata_element = metadata_elements[0]

        # Extract common metadata elements
        identifier = self._get_element_text(metadata_element, "./dc:identifier")
        title = self._get_element_text(metadata_element, "./dc:title")
        language = self._get_element_text(metadata_element, "./dc:language")

        # Extract creator and contributor lists
        creator = self._get_element_text_list(metadata_element, "./dc:creator")
        contributor = self._get_element_text_list(metadata_element, "./dc:contributor")

        # Extract other elements
        publisher = self._get_element_text(metadata_element, "./dc:publisher")
        description = self._get_element_text(metadata_element, "./dc:description")
        rights = self._get_element_text(metadata_element, "./dc:rights")

        # Extract dates
        publication_date = None
        modified = None

        date_elements = metadata_element.xpath(
            "./dc:date", namespaces={"dc": "http://purl.org/dc/elements/1.1/"}
        )
        for date_element in date_elements:
            date_text = date_element.text
            if not date_text:
                continue

            # Try to parse the date
            try:
                date_obj = datetime.fromisoformat(date_text.strip())
                # Determine if this is a publication date or modified date
                if (
                    date_element.get("{http://www.idpf.org/2007/opf}property")
                    == "dcterms:modified"
                ):
                    modified = date_obj
                else:
                    publication_date = date_obj
            except (ValueError, TypeError):
                # Skip dates that can't be parsed
                pass

        # Extract additional metadata
        extra = {}
        for element in metadata_element.xpath("./*"):
            if element.tag.startswith("{http://purl.org/dc/elements/1.1/}"):
                # Skip Dublin Core elements already handled
                continue

            # Add other metadata to the extra dict
            name = element.tag.split("}")[-1]
            if element.text:
                extra[name] = element.text.strip()

        # Create the metadata object
        self._metadata = EPUBMetadata(
            identifier=identifier or "",
            title=title or "",
            language=language or "",
            creator=creator,
            contributor=contributor,
            publisher=publisher,
            description=description,
            publication_date=publication_date,
            modified=modified,
            rights=rights,
            extra=extra,
        )

    def _parse_manifest(self, root: etree._Element) -> None:
        """Parse manifest from the package document.

        Args:
            root: The root element of the package document
        """
        # Find the manifest element
        manifest_elements = root.xpath("//*[local-name()='manifest']")
        if not manifest_elements:
            return

        manifest_element = manifest_elements[0]

        # Create a new manifest
        self._manifest = EPUBManifest()

        # Extract item elements
        for item_element in manifest_element.xpath(".//*[local-name()='item']"):
            id_value = item_element.get("id")
            href = item_element.get("href")
            media_type = item_element.get("media-type")

            if not id_value or not href or not media_type:
                # Skip items missing required attributes
                continue

            # Extract optional attributes
            fallback = item_element.get("fallback")
            media_overlay = item_element.get("media-overlay")

            # Extract properties
            properties_attr = item_element.get("properties")
            properties = properties_attr.split() if properties_attr else None

            # Create a manifest item
            item = ManifestItem(
                id=id_value,
                href=href,
                media_type=media_type,
                properties=properties,
                fallback=fallback,
                media_overlay=media_overlay,
            )

            # Add to the manifest
            self._manifest.add_item(item)

    def _parse_spine(self, root: etree._Element) -> None:
        """Parse spine from the package document.

        Args:
            root: The root element of the package document
        """
        # Find the spine element
        spine_elements = root.xpath("//*[local-name()='spine']")
        if not spine_elements:
            return

        spine_element = spine_elements[0]

        # Get the reading direction
        direction = spine_element.get("page-progression-direction", "ltr")

        # Create a new spine with the right direction
        self._spine = EPUBSpine(direction=direction)

        # Extract itemref elements
        for itemref_element in spine_element.xpath(".//*[local-name()='itemref']"):
            idref = itemref_element.get("idref")
            if not idref:
                # Skip itemrefs missing required attributes
                continue

            # Extract optional attributes
            id_value = itemref_element.get("id")
            linear = itemref_element.get("linear", "yes")

            # Extract properties
            properties_attr = itemref_element.get("properties")
            properties = properties_attr.split() if properties_attr else None

            # Create a spine item
            item = SpineItem(
                idref=idref, linear=linear, properties=properties, id=id_value
            )

            # Add to the spine
            self._spine.add_item(item)

    def _parse_collections(self, root: etree._Element) -> None:
        """Parse collections from the package document.

        Args:
            root: The root element of the package document
        """
        # Find collection elements
        collection_elements = root.xpath("//*[local-name()='collection']")

        # Reset collections
        self._collections = []

        # Process each collection
        for collection_element in collection_elements:
            role = collection_element.get("role")
            if not role:
                # Skip collections missing required attributes
                continue

            # Create a new collection
            collection = EPUBCollection(role=role)

            # Extract link elements
            for link_element in collection_element.xpath(".//*[local-name()='link']"):
                href = link_element.get("href")
                if href:
                    collection.add_item(href)

            # Add to the collections list
            self._collections.append(collection)

    def to_xml(self) -> str:
        """Convert the package document to XML.

        Returns:
            The package document as an XML string
        """
        # Create a new root element
        for prefix, uri in self._xmlns.items():
            if prefix is None:
                root = etree.Element("{" + uri + "}package")
            else:
                etree.register_namespace(prefix, uri)

        # Set attributes
        root.set("version", self._version)
        root.set("unique-identifier", self._unique_identifier)
        if self._direction != "default":
            root.set("dir", self._direction)

        # Add metadata
        metadata_element = etree.SubElement(root, "metadata")
        self._build_metadata(metadata_element)

        # Add manifest
        manifest_element = etree.SubElement(root, "manifest")
        self._build_manifest(manifest_element)

        # Add spine
        spine_element = etree.SubElement(root, "spine")
        self._build_spine(spine_element)

        # Add collections
        self._build_collections(root)

        # Convert to XML string
        tree = etree.ElementTree(root)
        return etree.tostring(
            tree, encoding="utf-8", xml_declaration=True, pretty_print=True
        ).decode("utf-8")

    def _build_metadata(self, parent: etree._Element) -> None:
        """Build metadata elements.

        Args:
            parent: The parent element to add metadata to
        """
        # Add required elements
        self._add_dc_element(
            parent,
            "identifier",
            self._metadata.identifier,
            {"id": self._unique_identifier},
        )
        self._add_dc_element(parent, "title", self._metadata.title)
        self._add_dc_element(parent, "language", self._metadata.language)

        # Add creator and contributor lists
        if self._metadata.creator:
            for creator in self._metadata.creator:
                self._add_dc_element(parent, "creator", creator)

        if self._metadata.contributor:
            for contributor in self._metadata.contributor:
                self._add_dc_element(parent, "contributor", contributor)

        # Add other elements
        if self._metadata.publisher:
            self._add_dc_element(parent, "publisher", self._metadata.publisher)

        if self._metadata.description:
            self._add_dc_element(parent, "description", self._metadata.description)

        if self._metadata.rights:
            self._add_dc_element(parent, "rights", self._metadata.rights)

        # Add dates
        if self._metadata.publication_date:
            self._add_dc_element(
                parent, "date", self._metadata.publication_date.isoformat()
            )

        if self._metadata.modified:
            modified_element = self._add_dc_element(
                parent, "date", self._metadata.modified.isoformat()
            )
            modified_element.set(
                "{http://www.idpf.org/2007/opf}property", "dcterms:modified"
            )

        # Add extra metadata
        for name, value in self._metadata.extra.items():
            meta_element = etree.SubElement(parent, "meta")
            meta_element.set("name", name)
            meta_element.set("content", value)

    def _build_manifest(self, parent: etree._Element) -> None:
        """Build manifest elements.

        Args:
            parent: The parent element to add manifest items to
        """
        for item in self._manifest.items:
            item_element = etree.SubElement(parent, "item")
            item_element.set("id", item.id)
            item_element.set("href", item.href)
            item_element.set("media-type", item.media_type)

            if item.properties:
                item_element.set("properties", " ".join(item.properties))

            if item.fallback:
                item_element.set("fallback", item.fallback)

            if item.media_overlay:
                item_element.set("media-overlay", item.media_overlay)

    def _build_spine(self, parent: etree._Element) -> None:
        """Build spine elements.

        Args:
            parent: The parent element to add spine items to
        """
        # Set the reading direction
        parent.set("page-progression-direction", self._spine.direction)

        for item in self._spine.items:
            itemref_element = etree.SubElement(parent, "itemref")
            itemref_element.set("idref", item.idref)

            if item.id:
                itemref_element.set("id", item.id)

            if item.linear != "yes":
                itemref_element.set("linear", item.linear)

            if item.properties:
                itemref_element.set("properties", " ".join(item.properties))

    def _build_collections(self, parent: etree._Element) -> None:
        """Build collection elements.

        Args:
            parent: The parent element to add collections to
        """
        for collection in self._collections:
            collection_element = etree.SubElement(parent, "collection")
            collection_element.set("role", collection.role)

            for item in collection.items:
                link_element = etree.SubElement(collection_element, "link")
                link_element.set("href", item)

    def _add_dc_element(
        self,
        parent: etree._Element,
        name: str,
        value: str,
        attributes: Optional[Dict[str, str]] = None,
    ) -> etree._Element:
        """Add a Dublin Core element.

        Args:
            parent: The parent element
            name: The element name
            value: The element value
            attributes: Optional attributes

        Returns:
            The created element
        """
        if not value:
            return None

        element = etree.SubElement(
            parent, f"{{http://purl.org/dc/elements/1.1/}}{name}"
        )
        element.text = value

        if attributes:
            for attr_name, attr_value in attributes.items():
                element.set(attr_name, attr_value)

        return element

    def _get_element_text(self, parent: etree._Element, xpath: str) -> Optional[str]:
        """Get text from an element.

        Args:
            parent: The parent element
            xpath: The XPath expression

        Returns:
            The element text, or None if not found
        """
        elements = parent.xpath(
            xpath, namespaces={"dc": "http://purl.org/dc/elements/1.1/"}
        )

        if elements and elements[0].text:
            return elements[0].text.strip()

        return None

    def _get_element_text_list(self, parent: etree._Element, xpath: str) -> List[str]:
        """Get text from multiple elements.

        Args:
            parent: The parent element
            xpath: The XPath expression

        Returns:
            List of element texts
        """
        result = []
        elements = parent.xpath(
            xpath, namespaces={"dc": "http://purl.org/dc/elements/1.1/"}
        )

        for element in elements:
            if element.text:
                result.append(element.text.strip())

        return result if result else None
