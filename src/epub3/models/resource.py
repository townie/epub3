"""Resource models for EPUB3 publications."""

from typing import Union


class Resource:
    """Represents any resource in the EPUB publication.

    Attributes:
        id: The identifier of the resource
        path: The path to the resource within the EPUB container
        media_type: The MIME type of the resource
        _data: The binary data of the resource
    """

    def __init__(self, id: str, path: str, media_type: str, data: bytes):
        """Initialize a resource.

        Args:
            id: The identifier of the resource
            path: The path to the resource within the EPUB container
            media_type: The MIME type of the resource
            data: The binary data of the resource
        """
        self._id = id
        self._path = path
        self._media_type = media_type
        self._data = data

    @property
    def id(self) -> str:
        """Get the resource ID.

        Returns:
            The resource identifier
        """
        return self._id

    @property
    def path(self) -> str:
        """Get the resource path.

        Returns:
            The path to the resource within the EPUB container
        """
        return self._path

    @property
    def media_type(self) -> str:
        """Get the resource media type.

        Returns:
            The MIME type of the resource
        """
        return self._media_type

    def get_data(self) -> bytes:
        """Get the resource data as bytes.

        Returns:
            The binary data of the resource
        """
        return self._data

    def get_text(self) -> str:
        """Get the resource data as text.

        Returns:
            The resource data decoded as UTF-8 text
        """
        return self._data.decode("utf-8")

    def set_data(self, data: Union[bytes, str]) -> None:
        """Set the resource data.

        Args:
            data: The new data for the resource, either as bytes or string
        """
        if isinstance(data, str):
            self._data = data.encode("utf-8")
        else:
            self._data = data


class FontResource(Resource):
    """Specialized resource for font handling.

    Attributes:
        _is_obfuscated: Flag indicating if the font is obfuscated
    """

    def __init__(
        self,
        id: str,
        path: str,
        media_type: str,
        data: bytes,
        is_obfuscated: bool = False,
    ):
        """Initialize a font resource.

        Args:
            id: The identifier of the resource
            path: The path to the resource within the EPUB container
            media_type: The MIME type of the resource
            data: The binary data of the resource
            is_obfuscated: Flag indicating if the font is obfuscated
        """
        super().__init__(id, path, media_type, data)
        self._is_obfuscated = is_obfuscated

    @property
    def is_obfuscated(self) -> bool:
        """Check if the font is obfuscated.

        Returns:
            True if the font is obfuscated, False otherwise
        """
        return self._is_obfuscated

    def obfuscate(self) -> None:
        """Obfuscate the font according to the EPUB spec."""
        if not self._is_obfuscated:
            # Placeholder for actual obfuscation logic
            # This would use the publication ID to create the obfuscation key
            # and apply it to the font data according to the EPUB spec
            # For now, we just set the flag
            self._is_obfuscated = True

    def deobfuscate(self) -> None:
        """Deobfuscate the font according to the EPUB spec."""
        if self._is_obfuscated:
            # Placeholder for actual deobfuscation logic
            # This would reverse the obfuscation process
            # For now, we just clear the flag
            self._is_obfuscated = False
