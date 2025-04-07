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

tests/                       # Test suite
├── __init__.py
├── core/                    # Tests for core functionality
│   ├── __init__.py
│   ├── test_extractors.py   # Tests for audio extractors
│   └── test_transcriber.py  # Tests for transcriber
└── utils/                   # Tests for utilities
    ├── __init__.py
    └── test_file_utils.py   # Tests for file utilities

transcribe.py                # Main entry point script
setup.py                     # Package installation configuration
requirements.txt             # Project dependencies
```

## File Descriptions

- **transcribe.py**: The main entry point script that users can run to transcribe files. It imports and uses the functionality from the `transcription_app` package.

- **transcription_app/core/transcriber.py**: Contains the `Transcriber` class that handles the transcription of audio and video files using OpenAI's Whisper model.

- **transcription_app/core/extractors.py**: Contains the `AudioExtractor` interface and `FFmpegAudioExtractor` implementation for extracting audio from video files.

- **transcription_app/config/settings.py**: Contains configuration settings for different environments (dev, test, prod).

- **transcription_app/utils/file_utils.py**: Contains utility functions for file operations.

- **transcription_app/cli.py**: Implements the command-line interface for the application.

## Usage

### Command Line Interface

```bash
python transcriber.py path/to/file.mp4 --model base --output transcription.txt
```

Options:
- `--model`: Choose model size (tiny, base, small, medium, large)
- `--output`: Specify output file (default: input filename with .txt extension)

### As a Library

```python
from transcriber import Transcriber

# Initialize with desired model size
transcriber = Transcriber(model_size="base")

# Transcribe a file
text = transcriber.transcribe_file("path/to/file.mp4")
print(text)

# Transcribe and save to file
output_path = transcriber.transcribe_and_save("path/to/file.mp4", "output.txt")
```

## Testing

Run the tests with pytest:

```bash
python -m pytest tests/
```

## License

MIT
