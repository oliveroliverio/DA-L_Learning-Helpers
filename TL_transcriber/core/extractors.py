"""
Audio extraction functionality for the transcription app.
"""

import os
import subprocess
import tempfile
from abc import ABC, abstractmethod


class AudioExtractor(ABC):
    """
    Abstract base class for audio extractors.
    """
    
    @abstractmethod
    def extract_audio(self, file_path):
        """
        Extract audio from a file.
        
        Args:
            file_path (str): Path to the file to extract audio from
            
        Returns:
            str: Path to the extracted audio file
        """
        pass


class FFmpegAudioExtractor(AudioExtractor):
    """
    Audio extractor that uses FFmpeg to extract audio from video files.
    """
    
    def extract_audio(self, file_path):
        """
        Extract audio from a video file using ffmpeg.
        
        Args:
            file_path (str): Path to the video file
            
        Returns:
            str: Path to the extracted audio file
        """
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Create a temporary file for the extracted audio
        temp_audio = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        temp_audio.close()
        
        # Use ffmpeg to extract audio
        command = [
            'ffmpeg', 
            '-i', file_path, 
            '-q:a', '0',  # Use high quality
            '-map', 'a',  # Extract only audio
            '-f', 'mp3',
            temp_audio.name
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            # Clean up the temporary file if extraction fails
            os.unlink(temp_audio.name)
            raise Exception(f"Failed to extract audio from video: {result.stderr}")
        
        return temp_audio.name
