"""
Tests for the extractors module.
"""

import os
import unittest
from unittest.mock import patch, MagicMock

from transcription_app.core.extractors import AudioExtractor, FFmpegAudioExtractor


class TestFFmpegAudioExtractor(unittest.TestCase):
    """Test cases for the FFmpegAudioExtractor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.extractor = FFmpegAudioExtractor()

    def tearDown(self):
        """Tear down test fixtures."""
        pass

    @patch('os.path.exists')
    def test_extract_audio_file_not_found(self, mock_exists):
        """Test extracting audio from a non-existent file."""
        # Mock file existence check
        mock_exists.return_value = False

        # Test that FileNotFoundError is raised for non-existent file
        with self.assertRaises(FileNotFoundError):
            self.extractor.extract_audio("non_existent_file.mp4")

    @patch('os.path.exists')
    @patch('tempfile.NamedTemporaryFile')
    @patch('subprocess.run')
    def test_extract_audio_success(self, mock_run, mock_tempfile, mock_exists):
        """Test successful audio extraction."""
        # Mock file existence check
        mock_exists.return_value = True

        # Mock temporary file
        mock_temp = MagicMock()
        mock_temp.name = "temp_audio.mp3"
        mock_tempfile.return_value = mock_temp

        # Mock subprocess run
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_run.return_value = mock_process

        # Test audio extraction
        result = self.extractor.extract_audio("test_video.mp4")

        # Check that subprocess.run was called with the correct arguments
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        command = args[0]
        self.assertEqual(command[0], 'ffmpeg')
        self.assertEqual(command[2], 'test_video.mp4')
        self.assertEqual(command[-1], 'temp_audio.mp3')

        # Check that the result is the path to the temporary file
        self.assertEqual(result, "temp_audio.mp3")

    @patch('os.path.exists')
    @patch('tempfile.NamedTemporaryFile')
    @patch('subprocess.run')
    @patch('os.unlink')
    def test_extract_audio_failure(self, mock_unlink, mock_run, mock_tempfile, mock_exists):
        """Test failed audio extraction."""
        # Mock file existence check
        mock_exists.return_value = True

        # Mock temporary file
        mock_temp = MagicMock()
        mock_temp.name = "temp_audio.mp3"
        mock_tempfile.return_value = mock_temp

        # Mock subprocess run to simulate failure
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stderr = "FFmpeg error"
        mock_run.return_value = mock_process

        # Test that Exception is raised for failed extraction
        with self.assertRaises(Exception):
            self.extractor.extract_audio("test_video.mp4")

        # Check that the temporary file was deleted
        mock_unlink.assert_called_once_with("temp_audio.mp3")


if __name__ == '__main__':
    unittest.main()
