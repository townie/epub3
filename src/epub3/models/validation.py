"""Validation models for EPUB3 publications."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ValidationError:
    """Represents a validation error.

    Attributes:
        message: The error message
        location: The location where the error occurred
        severity: The severity of the error (fatal, error, warning)
    """

    message: str
    location: str
    severity: str


@dataclass
class ValidationWarning:
    """Represents a validation warning.

    Attributes:
        message: The warning message
        location: The location where the warning occurred
    """

    message: str
    location: str


@dataclass
class ValidationResult:
    """Represents the result of a validation operation.

    Attributes:
        valid: Whether the validation passed
        errors: List of validation errors
        warnings: List of validation warnings
    """

    valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationWarning] = field(default_factory=list)

    def add_error(self, message: str, location: str, severity: str = "error") -> None:
        """Add an error to the validation result.

        Args:
            message: The error message
            location: The location where the error occurred
            severity: The severity of the error
        """
        self.errors.append(ValidationError(message, location, severity))
        self.valid = False

    def add_warning(self, message: str, location: str) -> None:
        """Add a warning to the validation result.

        Args:
            message: The warning message
            location: The location where the warning occurred
        """
        self.warnings.append(ValidationWarning(message, location))

    def merge(self, other: "ValidationResult") -> None:
        """Merge another validation result into this one.

        Args:
            other: The validation result to merge
        """
        self.valid = self.valid and other.valid
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
