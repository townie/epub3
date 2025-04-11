#!/usr/bin/env python
"""
Example script demonstrating how to validate an EPUB file.

This example validates an EPUB file and reports any errors or warnings.
"""

import os
import sys

from epub3 import EPUB


def main():
    # Check if an input EPUB file is provided
    if len(sys.argv) < 2:
        print("Usage: python validate_epub.py <path_to_epub>")
        sys.exit(1)

    input_epub_path = sys.argv[1]
    if not os.path.exists(input_epub_path):
        print(f"Error: The file {input_epub_path} does not exist.")
        sys.exit(1)

    # Create an EPUB processor
    epub_processor = EPUB()

    try:
        # Open the EPUB file
        epub = epub_processor.open(input_epub_path)

        # Display basic information
        print(f"Validating EPUB: {os.path.basename(input_epub_path)}")
        print(f"Title: {epub.metadata.title}")
        print(f"Identifier: {epub.metadata.identifier}")
        print()

        # Validate the EPUB
        result = epub_processor.validate(epub)

        # Display validation results
        if result.valid:
            print("✓ EPUB is valid!")
        else:
            print("✗ EPUB validation failed")

        # Display errors if any
        if result.errors:
            print("\nErrors:")
            for i, error in enumerate(result.errors, 1):
                print(f"{i}. [{error.severity}] {error.message}")
                print(f"   Location: {error.location}")

        # Display warnings if any
        if result.warnings:
            print("\nWarnings:")
            for i, warning in enumerate(result.warnings, 1):
                print(f"{i}. {warning.message}")
                print(f"   Location: {warning.location}")

        # Display summary
        print("\nValidation Summary:")
        print(f"- Errors: {len(result.errors)}")
        print(f"- Warnings: {len(result.warnings)}")

        # Provide suggestions for improving the EPUB if there are errors or warnings
        if result.errors or result.warnings:
            print("\nSuggestions for improvement:")
            if any(e.message.startswith("Missing") for e in result.errors):
                print(
                    "- Ensure all required metadata is present (identifier, title, language)"
                )
            if any("spine" in e.location for e in result.errors):
                print("- Check that the spine contains at least one item")
            if any("navigation" in w.location for w in result.warnings):
                print("- Add a navigation document with a table of contents")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        # Clean up resources
        epub_processor.close()


if __name__ == "__main__":
    main()
