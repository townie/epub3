"""Media overlay models for EPUB3 publications."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class AudioClip:
    """Represents an audio clip within a media overlay.

    Attributes:
        src: Source path to the audio file
        begin: Start time in seconds
        end: End time in seconds
    """

    src: str
    begin: float
    end: float

    @property
    def duration(self) -> float:
        """Get the duration of the audio clip.

        Returns:
            The duration in seconds
        """
        return self.end - self.begin


@dataclass
class MediaOverlayParallel:
    """Represents a parallel time container in a media overlay.

    A parallel time container synchronizes text with audio.

    Attributes:
        text_path: Path to the content document
        element_id: ID of the element within the content document
        audio_clip: The associated audio clip
        children: Optional list of child parallels for nested structures
    """

    text_path: str
    element_id: str
    audio_clip: AudioClip
    children: List["MediaOverlayParallel"] = field(default_factory=list)


class MediaOverlay:
    """Represents a media overlay document for text/audio synchronization.

    Attributes:
        _id: The media overlay ID
        _parallels: The list of parallel time containers
        _narrators: The list of narrators
        _text_to_parallel_map: A mapping from text element IDs to parallel containers
    """

    def __init__(self, id: str, narrators: Optional[List[str]] = None):
        """Initialize a media overlay.

        Args:
            id: The media overlay ID
            narrators: Optional list of narrators
        """
        self._id = id
        self._parallels: List[MediaOverlayParallel] = []
        self._narrators = narrators or []
        # Create a mapping for fast lookup of text elements
        self._text_to_parallel_map: Dict[str, MediaOverlayParallel] = {}

    @property
    def id(self) -> str:
        """Get the media overlay ID.

        Returns:
            The media overlay ID
        """
        return self._id

    @property
    def duration(self) -> float:
        """Get the total duration in seconds.

        Returns:
            The total duration of all audio clips
        """
        total_duration = 0.0
        for parallel in self._parallels:
            total_duration += parallel.audio_clip.duration
        return total_duration

    @property
    def narrators(self) -> List[str]:
        """Get the list of narrators.

        Returns:
            The list of narrator names
        """
        return self._narrators.copy()

    def get_parallels(self) -> List[MediaOverlayParallel]:
        """Get all parallel time containers.

        Returns:
            List of all parallel time containers
        """
        return self._parallels.copy()

    def get_audio_for_text_element(
        self, text_path: str, element_id: str
    ) -> Optional[AudioClip]:
        """Get the audio clip for a specific text element.

        Args:
            text_path: The path to the content document
            element_id: The ID of the element within the content document

        Returns:
            The audio clip, or None if not found
        """
        key = f"{text_path}#{element_id}"
        if key in self._text_to_parallel_map:
            return self._text_to_parallel_map[key].audio_clip
        return None

    def add_audio_clip(
        self, text_path: str, element_id: str, audio_src: str, begin: float, end: float
    ) -> None:
        """Add an audio clip for a text element.

        Args:
            text_path: The path to the content document
            element_id: The ID of the element within the content document
            audio_src: The path to the audio file
            begin: The start time in seconds
            end: The end time in seconds
        """
        audio_clip = AudioClip(audio_src, begin, end)
        parallel = MediaOverlayParallel(text_path, element_id, audio_clip)
        self._parallels.append(parallel)

        # Update the mapping
        key = f"{text_path}#{element_id}"
        self._text_to_parallel_map[key] = parallel
