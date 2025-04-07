"""
Tests for the file_utils module.
"""

import os
import unittest
from unittest.mock import patch, mock_open

from transcription_app.utils.file_utils import (
    ensure_directory_exists,
    get_file_extension,
    get_file_size,
    is_file_empty,
    safe_delete_file,
    get_base_filename
)


class TestFileUtils(unittest.TestCase):
    """Test cases for the file utility functions."""

    def test_get_file_extension(self):
        """Test getting file extension."""
        self.assertEqual(get_file_extension("test.mp3"), ".mp3")
        self.assertEqual(get_file_extension("test.MP3"), ".mp3")  # Test case insensitivity
        self.assertEqual(get_file_extension("path/to/test.mp4"), ".mp4")
        self.assertEqual(get_file_extension("test"), "")
        self.assertEqual(get_file_extension("test."), ".")

    @patch('os.path.getsize')
    def test_get_file_size(self, mock_getsize):
        """Test getting file size."""
        mock_getsize.return_value = 1024
        self.assertEqual(get_file_size("test.mp3"), 1024)
        mock_getsize.assert_called_once_with("test.mp3")

    @patch('transcription_app.utils.file_utils.get_file_size')
    def test_is_file_empty(self, mock_get_file_size):
        """Test checking if file is empty."""
        # Test empty file
        mock_get_file_size.return_value = 0
        self.assertTrue(is_file_empty("empty.txt"))
        
        # Test non-empty file
        mock_get_file_size.return_value = 100
        self.assertFalse(is_file_empty("non_empty.txt"))

    @patch('os.makedirs')
    def test_ensure_directory_exists(self, mock_makedirs):
        """Test ensuring directory exists."""
        ensure_directory_exists("test_dir")
        mock_makedirs.assert_called_once_with("test_dir", exist_ok=True)

    @patch('os.path.exists')
    @patch('os.unlink')
    def test_safe_delete_file(self, mock_unlink, mock_exists):
        """Test safely deleting a file."""
        # Test deleting existing file
        mock_exists.return_value = True
        safe_delete_file("existing.txt")
        mock_unlink.assert_called_once_with("existing.txt")
        
        # Test deleting non-existent file
        mock_exists.return_value = False
        mock_unlink.reset_mock()
        safe_delete_file("non_existent.txt")
        mock_unlink.assert_not_called()

    def test_get_base_filename(self):
        """Test getting base filename without extension."""
        self.assertEqual(get_base_filename("test.mp3"), "test")
        self.assertEqual(get_base_filename("path/to/test.mp4"), "test")
        self.assertEqual(get_base_filename("test"), "test")
        self.assertEqual(get_base_filename("test."), "test")


if __name__ == '__main__':
    unittest.main()
