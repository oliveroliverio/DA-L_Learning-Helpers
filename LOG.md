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
