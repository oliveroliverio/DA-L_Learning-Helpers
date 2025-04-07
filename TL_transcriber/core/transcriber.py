"""
Transcription functionality for the transcription app.
"""

import os
import whisper
from transcription_app.core.extractors import FFmpegAudioExtractor


class Transcriber:
    """
    A class to handle transcription of both audio and video files using OpenAI's Whisper model.
    """
    
    # Class constants for file extensions
    VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv']
    AUDIO_EXTENSIONS = ['.mp3', '.wav', '.ogg', '.flac', '.m4a']
    
    def __init__(self, model_size="base", model_factory=None, audio_extractor=None):
        """
        Initialize the Transcriber with a specified model size and dependencies.
        
        Args:
            model_size (str): Size of the Whisper model to use. 
                             Options: "tiny", "base", "small", "medium", "large"
            model_factory (callable, optional): Function to create the model.
                                              Defaults to whisper.load_model.
            audio_extractor (AudioExtractor, optional): Extractor for audio from video.
                                                      Defaults to FFmpegAudioExtractor.
        """
        self.model_size = model_size
        self.model = None
        self.model_factory = model_factory or whisper.load_model
        self.audio_extractor = audio_extractor or FFmpegAudioExtractor()
    
    def _load_model(self):
        """
        Load the Whisper model if it hasn't been loaded yet.
        """
        if self.model is None:
            self.model = self.model_factory(self.model_size)
    
    def is_video_file(self, file_path):
        """
        Check if the file is a video file based on its extension.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            bool: True if it's a video file, False otherwise
        """
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.VIDEO_EXTENSIONS
    
    def is_audio_file(self, file_path):
        """
        Check if the file is an audio file based on its extension.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            bool: True if it's an audio file, False otherwise
        """
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.AUDIO_EXTENSIONS
    
    def transcribe_file(self, file_path):
        """
        Transcribe an audio or video file.
        
        Args:
            file_path (str): Path to the audio or video file
            
        Returns:
            str: The transcribed text
        """
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Load the model if not already loaded
        self._load_model()
        
        # If it's a video file, extract the audio first
        if self.is_video_file(file_path):
            audio_path = self.audio_extractor.extract_audio(file_path)
            try:
                result = self.model.transcribe(audio_path)
                # Clean up the temporary audio file
                os.unlink(audio_path)
            except Exception as e:
                # Clean up on error too
                os.unlink(audio_path)
                raise e
        elif self.is_audio_file(file_path):
            # Directly transcribe audio file
            result = self.model.transcribe(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
        
        return result["text"]
    
    def transcribe_and_save(self, file_path, output_path=None):
        """
        Transcribe a file and save the result to a text file.
        
        Args:
            file_path (str): Path to the audio or video file
            output_path (str, optional): Path to save the transcription. 
                                        If None, will use the input filename with .txt extension
        
        Returns:
            str: Path to the saved transcription file
        """
        # Get transcription
        transcription = self.transcribe_file(file_path)
        
        # Determine output path if not provided
        if output_path is None:
            base_name = os.path.splitext(file_path)[0]
            output_path = f"{base_name}.txt"
        
        # Save transcription to file
        with open(output_path, 'w') as f:
            f.write(transcription)
        
        return output_path
