"""Layout management models for EPUB3 publications."""

from typing import Literal


class LayoutManager:
    """Handles fixed and reflowable layouts for EPUB publications.

    Attributes:
        _is_fixed_layout: Whether the publication uses fixed layout
        _orientation: The orientation setting
        _spread_behavior: The spread behavior setting
    """

    def __init__(
        self,
        is_fixed_layout: bool = False,
        orientation: Literal["auto", "portrait", "landscape"] = "auto",
        spread_behavior: Literal["auto", "none", "landscape"] = "auto",
    ):
        """Initialize the layout manager.

        Args:
            is_fixed_layout: Whether the publication uses fixed layout
            orientation: The orientation setting
            spread_behavior: The spread behavior setting
        """
        self._is_fixed_layout = is_fixed_layout
        self._orientation = orientation
        self._spread_behavior = spread_behavior

    @property
    def is_fixed_layout(self) -> bool:
        """Check if this is a fixed layout publication.

        Returns:
            True if the publication uses fixed layout, False otherwise
        """
        return self._is_fixed_layout

    @property
    def orientation(self) -> Literal["auto", "portrait", "landscape"]:
        """Get the orientation setting.

        Returns:
            The orientation setting: "auto", "portrait", or "landscape"
        """
        return self._orientation

    @property
    def spread_behavior(self) -> Literal["auto", "none", "landscape"]:
        """Get the spread behavior setting.

        Returns:
            The spread behavior setting: "auto", "none", or "landscape"
        """
        return self._spread_behavior

    def set_fixed_layout(self, is_fixed: bool) -> None:
        """Set whether this is a fixed layout publication.

        Args:
            is_fixed: Whether the publication uses fixed layout
        """
        self._is_fixed_layout = is_fixed

    def set_orientation(
        self, orientation: Literal["auto", "portrait", "landscape"]
    ) -> None:
        """Set the orientation setting.

        Args:
            orientation: The orientation setting

        Raises:
            ValueError: If the orientation value is invalid
        """
        if orientation not in ["auto", "portrait", "landscape"]:
            raise ValueError("Orientation must be 'auto', 'portrait', or 'landscape'")
        self._orientation = orientation

    def set_spread_behavior(
        self, behavior: Literal["auto", "none", "landscape"]
    ) -> None:
        """Set the spread behavior setting.

        Args:
            behavior: The spread behavior setting

        Raises:
            ValueError: If the behavior value is invalid
        """
        if behavior not in ["auto", "none", "landscape"]:
            raise ValueError("Spread behavior must be 'auto', 'none', or 'landscape'")
        self._spread_behavior = behavior
