import os
import subprocess
import tempfile
import whisper

class Transcriber:
    """
    A class to handle transcription of both audio and video files using OpenAI's Whisper model.
    """
    
    def __init__(self, model_size="base"):
        """
        Initialize the Transcriber with a specified model size.
        
        Args:
            model_size (str): Size of the Whisper model to use. 
                             Options: "tiny", "base", "small", "medium", "large"
        """
        self.model_size = model_size
        self.model = None
        self.video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv']
        self.audio_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.m4a']
    
    def _load_model(self):
        """
        Load the Whisper model if it hasn't been loaded yet.
        """
        if self.model is None:
            self.model = whisper.load_model(self.model_size)
    
    def _is_video_file(self, file_path):
        """
        Check if the file is a video file based on its extension.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            bool: True if it's a video file, False otherwise
        """
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.video_extensions
    
    def _extract_audio_from_video(self, video_path):
        """
        Extract audio from a video file using ffmpeg.
        
        Args:
            video_path (str): Path to the video file
            
        Returns:
            str: Path to the extracted audio file
        """
        # Create a temporary file for the extracted audio
        temp_audio = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        temp_audio.close()
        
        # Use ffmpeg to extract audio
        command = [
            'ffmpeg', 
            '-i', video_path, 
            '-q:a', '0',  # Use high quality
            '-map', 'a',  # Extract only audio
            '-f', 'mp3',
            temp_audio.name
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Failed to extract audio from video: {result.stderr}")
        
        return temp_audio.name
    
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
        if self._is_video_file(file_path):
            audio_path = self._extract_audio_from_video(file_path)
            try:
                result = self.model.transcribe(audio_path)
                # Clean up the temporary audio file
                os.unlink(audio_path)
            except Exception as e:
                # Clean up on error too
                os.unlink(audio_path)
                raise e
        else:
            # Directly transcribe audio file
            result = self.model.transcribe(file_path)
        
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


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Transcribe audio and video files using OpenAI's Whisper")
    parser.add_argument("file", help="Path to the audio or video file to transcribe")
    parser.add_argument("--model", choices=["tiny", "base", "small", "medium", "large"], 
                        default="base", help="Whisper model size to use")
    parser.add_argument("--output", help="Path to save the transcription (default: input filename with .txt extension)")
    
    args = parser.parse_args()
    
    transcriber = Transcriber(model_size=args.model)
    output_path = transcriber.transcribe_and_save(args.file, args.output)
    
    print(f"Transcription saved to: {output_path}")
