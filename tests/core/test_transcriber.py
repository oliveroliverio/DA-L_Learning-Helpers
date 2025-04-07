"""
Tests for the transcriber module.
"""

import os
import unittest
from unittest.mock import patch, MagicMock

from transcription_app.core.transcriber import Transcriber


class TestTranscriber(unittest.TestCase):
    """Test cases for the Transcriber class."""

    def setUp(self):
        """Set up test fixtures."""
        self.transcriber = Transcriber(model_size="tiny")

    def tearDown(self):
        """Tear down test fixtures."""
        pass

    @patch('transcription_app.core.transcriber.whisper')
    def test_load_model(self, mock_whisper):
        """Test loading the model."""
        # Mock the whisper.load_model method
        mock_model = MagicMock()
        mock_whisper.load_model.return_value = mock_model

        # Test that the model is loaded correctly
        self.transcriber._load_model()
        mock_whisper.load_model.assert_called_once_with("tiny")
        self.assertEqual(self.transcriber.model, mock_model)

    @patch('transcription_app.core.transcriber.whisper')
    @patch('os.path.exists')
    def test_transcribe_audio_file(self, mock_exists, mock_whisper):
        """Test transcribing an audio file."""
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

    @patch('transcription_app.core.transcriber.whisper')
    @patch('os.path.exists')
    def test_transcribe_video_file(self, mock_exists, mock_whisper):
        """Test transcribing a video file."""
        # Mock file existence check
        mock_exists.return_value = True

        # Mock the audio extractor
        mock_extractor = MagicMock()
        mock_extractor.extract_audio.return_value = "temp_audio.mp3"
        self.transcriber.audio_extractor = mock_extractor

        # Mock the model and its transcribe method
        mock_model = MagicMock()
        result_text = "This is a test video transcription"
        mock_model.transcribe.return_value = {"text": result_text}
        mock_whisper.load_model.return_value = mock_model

        # Initialize the model
        self.transcriber._load_model()

        # Test transcription of a video file
        with patch('os.unlink') as mock_unlink:
            result = self.transcriber.transcribe_file("test_video.mp4")

        # Check that the audio extractor was called
        mock_extractor.extract_audio.assert_called_once_with("test_video.mp4")

        # Check that the model transcribed the extracted audio
        mock_model.transcribe.assert_called_once_with("temp_audio.mp3")

        # Check that the temporary file was deleted
        mock_unlink.assert_called_once_with("temp_audio.mp3")

        # Check the result
        self.assertEqual(result, result_text)

    def test_is_video_file(self):
        """Test video file detection."""
        self.assertTrue(self.transcriber.is_video_file("test.mp4"))
        self.assertTrue(self.transcriber.is_video_file("test.avi"))
        self.assertTrue(self.transcriber.is_video_file("test.mkv"))
        self.assertFalse(self.transcriber.is_video_file("test.mp3"))
        self.assertFalse(self.transcriber.is_video_file("test.wav"))

    def test_is_audio_file(self):
        """Test audio file detection."""
        self.assertTrue(self.transcriber.is_audio_file("test.mp3"))
        self.assertTrue(self.transcriber.is_audio_file("test.wav"))
        self.assertTrue(self.transcriber.is_audio_file("test.ogg"))
        self.assertFalse(self.transcriber.is_audio_file("test.mp4"))
        self.assertFalse(self.transcriber.is_audio_file("test.txt"))


if __name__ == '__main__':
    unittest.main()
