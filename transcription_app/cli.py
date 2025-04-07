"""
Command-line interface for the transcription app.
"""

import argparse
import os
import sys
from transcription_app.core.transcriber import Transcriber
from transcription_app.config.settings import MODEL_SIZES, DEFAULT_MODEL_SIZE


def parse_args():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Transcribe audio and video files using OpenAI's Whisper"
    )
    
    parser.add_argument(
        "file",
        help="Path to the audio or video file to transcribe"
    )
    
    parser.add_argument(
        "--model",
        choices=MODEL_SIZES,
        default=DEFAULT_MODEL_SIZE,
        help=f"Whisper model size to use (default: {DEFAULT_MODEL_SIZE})"
    )
    
    parser.add_argument(
        "--output",
        help="Path to save the transcription (default: input filename with .txt extension)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()


def main():
    """
    Main entry point for the CLI.
    """
    args = parse_args()
    
    # Check if file exists
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    
    try:
        # Initialize transcriber
        transcriber = Transcriber(model_size=args.model)
        
        if args.verbose:
            print(f"Transcribing {args.file} with model size {args.model}...")
        
        # Transcribe and save
        output_path = transcriber.transcribe_and_save(args.file, args.output)
        
        print(f"Transcription saved to: {output_path}")
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
