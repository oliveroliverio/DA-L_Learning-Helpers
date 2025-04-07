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
