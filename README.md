# Audio/Video Transcription Tool

A Python application that uses OpenAI's Whisper model to transcribe both audio and video files. The application follows test-driven development practices.

## Features

- Transcribe audio files (mp3, wav, ogg, flac, m4a)
- Transcribe video files (mp4, avi, mov, mkv, webm, flv)
- Command-line interface for easy use
- Configurable model size for different accuracy/performance tradeoffs

## Requirements

- Python 3.12+
- FFmpeg (for video file processing)
- OpenAI Whisper

## Installation

1. Clone the repository
2. Create a virtual environment and install dependencies:

```bash
uv venv && source .venv/bin/activate && uv pip install -r requirements.txt
```

3. Make sure FFmpeg is installed on your system:
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Project Structure

The project follows a modular architecture:

```
transcription_app/           # Main package
├── __init__.py              # Package initialization
├── cli.py                   # Command-line interface
├── config/                  # Configuration settings
│   ├── __init__.py
│   └── settings.py          # Environment-specific settings
├── core/                    # Core functionality
│   ├── __init__.py
│   ├── extractors.py        # Audio extraction from video files
│   └── transcriber.py       # Main transcription functionality
└── utils/                   # Utility functions
    ├── __init__.py
    └── file_utils.py        # File operation utilities
    └── prep_for_json.py     # Prepares transcription data for JSON output

tests/                       # Test suite
├── __init__.py
├── core/                    # Tests for core functionality
│   ├── __init__.py
│   ├── test_extractors.py   # Tests for audio extractors
│   └── test_transcriber.py  # Tests for transcriber
└── utils/                   # Tests for utilities
    ├── __init__.py
    └── test_file_utils.py   # Tests for file utilities
    └── test_prep_for_json.py # Tests for prep_for_json

transcribe.py                # Main entry point script
setup.py                     # Package installation configuration
requirements.txt             # Project dependencies

## Learning Sessions

The `prep_for_json.py` script helps prepare markdown content (such as ChatGPT conversations) for JSON storage by:

1. Escaping double quotes to ensure JSON compatibility
2. Removing excessive blank lines to improve readability
3. Saving the processed content to a new file with `_esc_dblqts` suffix

### Usage

```bash
# Process a markdown file
python prep_for_json.py -f path/to/markdown_file.md

# Process content from clipboard
python prep_for_json.py

# Test JSON compatibility
python prep_for_json.py -f path/to/markdown_file.md -t
```

The script can be used to prepare learning session content for storage in a structured JSON format, making it easier to build a knowledge base from your conversations.
