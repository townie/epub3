"""Main EPUB class for reading, creating, and writing EPUB files."""

import io
import os
import shutil
import tempfile
import zipfile
from typing import Any, BinaryIO, Dict, Optional, Union

from lxml import etree

from epub3.models.container import EPUBContainer
from epub3.models.manifest import ManifestItem
from epub3.models.metadata import EPUBMetadata
from epub3.models.package_document import PackageDocument
from epub3.models.resource import Resource
from epub3.models.validation import ValidationResult


class EPUB:
    """Primary class for reading, parsing, creating, and writing EPUB files.

    Attributes:
        _temp_dir: Temporary directory for extracted EPUB files
        _options: Options for EPUB processing
    """

    def __init__(self, options: Optional[Dict[str, Any]] = None):
        """Initialize the EPUB processor with optional configuration.

        Args:
            options: Optional configuration options
        """
        self._temp_dir: Optional[str] = None
        self._options = options or {}

    def open(self, source: Union[str, BinaryIO, bytes]) -> EPUBContainer:
        """Open an EPUB file from a file path, file-like object, or bytes.

        Args:
            source: The EPUB source (file path, file-like object, or bytes)

        Returns:
            The EPUB container

        Raises:
            ValueError: If the EPUB file is invalid
            IOError: If there's an issue reading the file
        """
        # Create a temporary directory for extraction
        self._create_temp_dir()

        try:
            # Handle different source types
            if isinstance(source, str):
                # File path
                with zipfile.ZipFile(source, "r") as zip_file:
                    self._extract_epub(zip_file)
            elif isinstance(source, bytes):
                # Bytes
                with zipfile.ZipFile(io.BytesIO(source), "r") as zip_file:
                    self._extract_epub(zip_file)
            else:
                # File-like object
                with zipfile.ZipFile(source, "r") as zip_file:
                    self._extract_epub(zip_file)

            # Parse the EPUB container
            return self._parse_container()

        except Exception as e:
            # Clean up and re-raise the exception
            self.close()
            raise ValueError(f"Error opening EPUB file: {str(e)}")

    def create(self, metadata: EPUBMetadata) -> EPUBContainer:
        """Create a new EPUB container with the provided metadata.

        Args:
            metadata: The metadata for the new EPUB

        Returns:
            The new EPUB container
        """
        # Create a temporary directory for the new EPUB
        self._create_temp_dir()

        try:
            # Create the OCF structure
            os.makedirs(os.path.join(self._temp_dir, "META-INF"))

            # Create the container.xml file
            self._create_container_xml()

            # Create the package document with the provided metadata
            package_doc = PackageDocument(metadata)

            # Create the EPUB container
            container = EPUBContainer(package_doc)

            return container

        except Exception as e:
            # Clean up and re-raise the exception
            self.close()
            raise ValueError(f"Error creating EPUB: {str(e)}")

    def write(self, epub: EPUBContainer, destination: Union[str, BinaryIO]) -> None:
        """Write the EPUB to a file path or file-like object.

        Args:
            epub: The EPUB container to write
            destination: The destination (file path or file-like object)

        Raises:
            ValueError: If there's an issue writing the EPUB
        """
        try:
            # Update the package document in the temporary directory
            self._write_package_document(epub)

            # Write the content documents
            self._write_content_documents(epub)

            # Create the ZIP file
            if isinstance(destination, str):
                # File path
                with zipfile.ZipFile(
                    destination, "w", zipfile.ZIP_DEFLATED
                ) as zip_file:
                    self._write_epub_zip(zip_file)
            else:
                # File-like object
                with zipfile.ZipFile(
                    destination, "w", zipfile.ZIP_DEFLATED
                ) as zip_file:
                    self._write_epub_zip(zip_file)

        except Exception as e:
            raise ValueError(f"Error writing EPUB: {str(e)}")

    def add_content(self, epub: EPUBContainer, content: "XHTMLDocument") -> None:
        """Add content to the EPUB container.

        Args:
            epub: The EPUB container
            content: The content document to add

        Raises:
            ValueError: If there's an issue adding the content
        """
        try:
            # Create a resource for the content
            resource = Resource(
                id=content.id,
                path=content.path,
                media_type=content.media_type,
                data=content.save(),
            )

            # Add the resource to the container
            epub.add_resource(resource)

            # Add the content to the manifest
            manifest_item = ManifestItem(
                id=content.id, href=content.path, media_type=content.media_type
            )
            epub.manifest.add_item(manifest_item)

        except Exception as e:
            raise ValueError(f"Error adding content: {str(e)}")

    def validate(self, epub: EPUBContainer) -> ValidationResult:
        """Validate the EPUB file against the EPUB specification.

        Args:
            epub: The EPUB container to validate

        Returns:
            The validation result
        """
        # Placeholder for actual validation
        # In a real implementation, this would use the EPUB spec to validate the file
        result = ValidationResult(valid=True)

        # For now, do some basic validation

        # Check required metadata
        if not epub.metadata.identifier:
            result.add_error("Missing identifier in metadata", "metadata")

        if not epub.metadata.title:
            result.add_error("Missing title in metadata", "metadata")

        if not epub.metadata.language:
            result.add_error("Missing language in metadata", "metadata")

        # Check spine
        if not epub.spine.items:
            result.add_error("Empty spine", "spine")

        # Check for required files
        if not epub.get_navigation():
            result.add_warning("No navigation document found", "navigation")

        return result

    def close(self) -> None:
        """Close and clean up any resources."""
        if self._temp_dir and os.path.exists(self._temp_dir):
            shutil.rmtree(self._temp_dir)
            self._temp_dir = None

    def _create_temp_dir(self) -> None:
        """Create a temporary directory for EPUB extraction."""
        if self._temp_dir:
            self.close()

        self._temp_dir = tempfile.mkdtemp()

    def _extract_epub(self, zip_file: zipfile.ZipFile) -> None:
        """Extract the EPUB zip file to the temporary directory.

        Args:
            zip_file: The EPUB zip file

        Raises:
            ValueError: If the EPUB file is invalid
        """
        # Check for required OCF files
        if "mimetype" not in zip_file.namelist():
            raise ValueError("Invalid EPUB: missing mimetype file")

        if "META-INF/container.xml" not in zip_file.namelist():
            raise ValueError("Invalid EPUB: missing container.xml file")

        # Extract all files
        zip_file.extractall(self._temp_dir)

        # Check mimetype content
        with open(os.path.join(self._temp_dir, "mimetype"), "r") as f:
            mimetype = f.read().strip()
            if mimetype != "application/epub+zip":
                raise ValueError(f"Invalid EPUB: incorrect mimetype: {mimetype}")

    def _parse_container(self) -> EPUBContainer:
        """Parse the EPUB container from the extracted files.

        Returns:
            The EPUB container

        Raises:
            ValueError: If there's an issue parsing the container
        """
        # Parse container.xml to get the package document path
        container_path = os.path.join(self._temp_dir, "META-INF", "container.xml")
        package_path = self._get_package_path(container_path)

        # Parse the package document
        package_doc = self._parse_package_document(package_path)

        # Create the EPUB container
        container = EPUBContainer(package_doc)

        # Load all resources and parse content documents
        self._load_resources(container, os.path.dirname(package_path))

        return container

    def _get_package_path(self, container_path: str) -> str:
        """Get the package document path from container.xml.

        Args:
            container_path: Path to container.xml

        Returns:
            The package document path

        Raises:
            ValueError: If the package document path can't be found
        """
        try:
            tree = etree.parse(container_path)
            root = tree.getroot()

            # Find the rootfile element
            rootfiles = root.xpath(
                "//*[local-name()='rootfile' and @media-type='application/oebps-package+xml']"
            )

            if not rootfiles:
                raise ValueError("No rootfile found in container.xml")

            # Get the full-path attribute
            full_path = rootfiles[0].get("full-path")
            if not full_path:
                raise ValueError("No full-path attribute in rootfile")

            # Return the absolute path
            return os.path.join(self._temp_dir, full_path)

        except Exception as e:
            raise ValueError(f"Error parsing container.xml: {str(e)}")

    def _parse_package_document(self, package_path: str) -> PackageDocument:
        """Parse the package document from the given path.

        Args:
            package_path: Path to the package document

        Returns:
            The package document

        Raises:
            ValueError: If there's an issue parsing the package document
        """
        try:
            with open(package_path, "r", encoding="utf-8") as f:
                xml = f.read()

            return PackageDocument.parse(xml)

        except Exception as e:
            raise ValueError(f"Error parsing package document: {str(e)}")

    def _load_resources(self, container: EPUBContainer, base_dir: str) -> None:
        """Load all resources and parse content documents.

        Args:
            container: The EPUB container
            base_dir: The base directory for relative paths

        Raises:
            ValueError: If there's an issue loading resources
        """
        try:
            # Process all manifest items
            for item in container.manifest.items:
                # Get the absolute path of the resource
                item_path = os.path.normpath(os.path.join(base_dir, item.href))

                # Read the resource data
                with open(item_path, "rb") as f:
                    data = f.read()

                # Create a resource
                resource = Resource(
                    id=item.id, path=item.href, media_type=item.media_type, data=data
                )

                # Add the resource to the container
                container.add_resource(resource)

        except Exception as e:
            raise ValueError(f"Error loading resources: {str(e)}")

    def _create_container_xml(self) -> None:
        """Create the container.xml file in the META-INF directory."""
        container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="content/package.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""
        with open(
            os.path.join(self._temp_dir, "META-INF", "container.xml"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(container_xml)

        # Create mimetype file
        with open(os.path.join(self._temp_dir, "mimetype"), "w", encoding="utf-8") as f:
            f.write("application/epub+zip")

        # Create content directory
        os.makedirs(os.path.join(self._temp_dir, "content"))

    def _write_package_document(self, epub: EPUBContainer) -> None:
        """Write the package document to the temporary directory.

        Args:
            epub: The EPUB container
        """
        # Get the package document XML
        xml = epub.get_package_document().to_xml()

        # Write to the file
        package_path = os.path.join(self._temp_dir, "content", "package.opf")
        os.makedirs(os.path.dirname(package_path), exist_ok=True)

        with open(package_path, "w", encoding="utf-8") as f:
            f.write(xml)

    def _write_content_documents(self, epub: EPUBContainer) -> None:
        """Write content documents and resources to the temporary directory.

        Args:
            epub: The EPUB container
        """
        for resource_path, resource in epub._resources.items():
            # Get the absolute path
            abs_path = os.path.join(self._temp_dir, resource_path)

            # Create parent directories if needed
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)

            # Write the resource data
            with open(abs_path, "wb") as f:
                f.write(resource.get_data())

    def _write_epub_zip(self, zip_file: zipfile.ZipFile) -> None:
        """Write all files to the ZIP file.

        Args:
            zip_file: The ZIP file to write to
        """
        # Write mimetype first and uncompressed
        mimetype_path = os.path.join(self._temp_dir, "mimetype")
        zip_file.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)

        # Walk the temporary directory and add all other files
        for root, _, files in os.walk(self._temp_dir):
            for file in files:
                if file == "mimetype":
                    continue  # Already added

                # Get the absolute path
                abs_path = os.path.join(root, file)

                # Get the relative path for the ZIP
                rel_path = os.path.relpath(abs_path, self._temp_dir)

                # Add to the ZIP
                zip_file.write(abs_path, rel_path)
