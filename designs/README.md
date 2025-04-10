# EPUB Library Architecture Diagrams

This directory contains software architecture diagrams for the EPUB library based on the PRD requirements and the planned high-level API. These diagrams provide a visual representation of the system's structure, components, interactions, and data flows.

## Table of Diagrams

1. **Class Diagram** (01_class_diagram.md)
   - Provides an overview of the key classes and their relationships
   - Shows attributes and methods of each class
   - Illustrates inheritance hierarchies

2. **EPUB Reading Flow** (02_epub_reading_flow.md)
   - Sequence diagram for reading/parsing an EPUB file
   - Shows interaction between components during the reading process
   - Details the extraction of package, navigation, and content documents

3. **EPUB Creation Flow** (03_epub_creation_flow.md)
   - Sequence diagram for creating a new EPUB publication
   - Shows the process from metadata creation to writing the final container
   - Illustrates how resources are added and organized

4. **Package Document Flow** (04_package_document_flow.md)
   - Flowchart for package document operations
   - Shows reading, writing, and manipulation processes
   - Details metadata, manifest, and spine operations

5. **Navigation Document Flow** (05_navigation_document_flow.md)
   - Flowchart for navigation document operations
   - Shows TOC, page list, and landmarks handling
   - Details creation and modification processes

6. **Validation Flow** (06_validation_flow.md)
   - Sequence diagram for EPUB validation
   - Shows validation of different EPUB components
   - Illustrates error collection and reporting

7. **Component Diagram** (07_component_diagram.md)
   - High-level view of system components
   - Shows relationships between modules
   - Links components to use cases and external dependencies

8. **Media Overlay Flow** (08_media_overlay_flow.md)
   - Flowchart for media overlay operations
   - Shows parsing, creation, and playback processes
   - Details synchronization between text and audio

9. **Use Case Diagram** (09_usecase_diagram.md)
   - Maps use cases to API components
   - Shows how different client requirements are fulfilled
   - Links requirements to implementation classes

## Using These Diagrams

- The diagrams are created using the Mermaid markdown syntax
- They can be viewed in GitHub or any Mermaid-compatible markdown viewer
- They provide different perspectives on the architecture:
  - Structural (class and component diagrams)
  - Behavioral (sequence and flow diagrams)
  - Functional (use case diagram)

These diagrams serve as a reference for developers implementing the EPUB library, giving them a clear understanding of the system architecture and component interactions.
