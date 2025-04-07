# Development Log

## 2025-04-06: Updated requirements.txt for slide extractor modules

### Changes:
- Added new dependencies to requirements.txt for the TL_slide_extractor module:
  - opencv-python>=4.8.0
  - numpy>=1.24.0
  - mss>=7.0.0
  - pytesseract>=0.3.10
  - scikit-image>=0.20.0

### Files Changed:
- requirements.txt

## 2025-04-06: Created new branch for slide extractor development

### Changes:
- Created a new branch "TL-slide_extractor" for isolating slide extractor development
- Pushed the branch to remote repository

### Files Changed:
- No files changed, only branch management

## 2025-04-06: Added unit tests for slide extractor image similarity

### Changes:
- Created a new test directory structure for slide extractor tests
- Implemented unit tests to verify image similarity between consecutive screen captures
- Tests confirm that consecutive captures from monitor 2 have high similarity (score: 0.97)
- Added test for perfect similarity with identical images

### Files Changed:
- tests/slide_extractor/__init__.py (new file)
- tests/slide_extractor/test_image_similarity.py (new file)

## 2025-04-06: Added image deletion functionality to slide extractor

### Changes:
- Added configuration option DELETE_IMAGES_AFTER_OCR (default: True) to control image deletion
- Modified the OCR worker to delete image files after OCR processing is complete
- Added error handling for file deletion operations
- Images are now deleted in all cases: successful OCR, no text extracted, and processing errors
- This change reduces disk space usage as only the extracted text is kept

### Files Changed:
- TL_slide_extractor/slide_extractor.py

## 2025-04-06: Enhanced OCR processing to handle dark mode

### Changes:
- Added support for dark mode text recognition (light text on dark backgrounds)
- Implemented dual-path OCR processing for both light and dark mode
- Added image inversion for dark mode processing
- Added CLAHE (Contrast Limited Adaptive Histogram Equalization) for better contrast in dark mode
- Added configuration options to control OCR behavior:
  - MIN_TEXT_LENGTH: Minimum text length to consider OCR successful
  - TRY_DARK_MODE: Whether to try both light and dark mode processing
- Changed output directory from "captured_slides" to "captured_text" to better reflect content
- Fixed various code style issues and improved code organization

### Files Changed:
- TL_slide_extractor/slide_extractor.py

## 2025-04-06: Merged slide extractor enhancements to main branch

### Changes:
- Merged the TL-slide_extractor branch into the main branch
- All slide extractor enhancements are now available in the main codebase:
  - Dark mode OCR processing support
  - Image deletion functionality
  - Unit tests for image similarity

### Files Changed:
- No direct file changes, only branch management

## 2025-04-06: Created JSON-Friendly Markdown GUI

### Changes:
- Created a GUI application for converting raw markdown to JSON-friendly format
- Features include:
  - Two-panel interface with raw markdown input and JSON-friendly output
  - Drag and drop support for markdown files
  - Automatic processing as you type
  - Option to convert newlines to literal "\n" strings
  - Copy button for easy clipboard access
- Added PyQt5 dependency to requirements.txt

### Files Changed:
- TL_json-friendly-markdown/json_markdown_gui.py (new file)
- TL_json-friendly-markdown/README.md (new file)
- requirements.txt

## 2025-04-06: Created Learning Session Database Module

### Changes:
- Created a new module TL_learning-session-database for storing learning sessions in SQLite
- Implemented a database manager with CRUD operations for learning sessions
- Added SQLAlchemy ORM support as an alternative approach
- Created a migration script to convert existing JSON data to SQLite
- Added comprehensive unit tests for database operations
- Set up proper directory structure following best practices:
  - database/ - Core database functionality
  - data/ - For storing the SQLite database file
  - tests/ - Unit tests for database operations

### Files Changed:
- TL_learning-session-database/README.md (new file)
- TL_learning-session-database/.gitignore (new file)
- TL_learning-session-database/database/__init__.py (new file)
- TL_learning-session-database/database/db_manager.py (new file)
- TL_learning-session-database/database/models.py (new file)
- TL_learning-session-database/database/migrations/__init__.py (new file)
- TL_learning-session-database/json_to_sqlite.py (new file)
- TL_learning-session-database/tests/test_db.py (new file)
