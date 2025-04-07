import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import our module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transcriber import Transcriber


class TestTranscriber(unittest.TestCase):
    
    def setUp(self):
        # Set up any resources needed for tests
        self.transcriber = Transcriber(model_size="tiny")
    
    def tearDown(self):
        # Clean up any resources after tests
        pass
    
    @patch('transcriber.whisper')
    def test_load_model(self, mock_whisper):
        # Mock the whisper.load_model method
        mock_model = MagicMock()
        mock_whisper.load_model.return_value = mock_model
        
        # Test that the model is loaded correctly
        self.transcriber._load_model()
        mock_whisper.load_model.assert_called_once_with("tiny")
        self.assertEqual(self.transcriber.model, mock_model)
    
    @patch('transcriber.whisper')
    @patch('os.path.exists')
    def test_transcribe_audio_file(self, mock_exists, mock_whisper):
        # Mock file existence check
        mock_exists.return_value = True
        
        # Mock the model and its transcribe method
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {"text": "This is a test transcription"}
        mock_whisper.load_model.return_value = mock_model
        
        # Initialize the model
        self.transcriber._load_model()
        
        # Test transcription of an audio file
        result = self.transcriber.transcribe_file("test_audio.mp3")
        mock_model.transcribe.assert_called_once_with("test_audio.mp3")
        self.assertEqual(result, "This is a test transcription")
    
    @patch('transcriber.whisper')
    @patch('transcriber.subprocess')
    @patch('os.path.exists')
    def test_transcribe_video_file(self, mock_exists, mock_subprocess, mock_whisper):
        # Mock file existence check
        mock_exists.return_value = True
        
        # Mock subprocess to simulate extracting audio from video
        mock_subprocess.run.return_value = MagicMock(returncode=0)
        
        # Mock the model and its transcribe method
        mock_model = MagicMock()
        result_text = "This is a test video transcription"
        mock_model.transcribe.return_value = {"text": result_text}
        mock_whisper.load_model.return_value = mock_model
        
        # Initialize the model
        self.transcriber._load_model()
        
        # Test transcription of a video file
        result = self.transcriber.transcribe_file("test_video.mp4")
        
        # Check that subprocess was called to extract audio
        mock_subprocess.run.assert_called_once()
        
        # Check that the model transcribed the extracted audio
        self.assertEqual(result, result_text)
    
    def test_is_video_file(self):
        # Test video file detection
        self.assertTrue(self.transcriber._is_video_file("test.mp4"))
        self.assertTrue(self.transcriber._is_video_file("test.avi"))
        self.assertTrue(self.transcriber._is_video_file("test.mkv"))
        self.assertFalse(self.transcriber._is_video_file("test.mp3"))
        self.assertFalse(self.transcriber._is_video_file("test.wav"))


if __name__ == '__main__':
    unittest.main()
