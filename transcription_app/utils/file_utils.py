"""
File utility functions for the transcription app.
"""

import os
import shutil
from pathlib import Path


def ensure_directory_exists(directory_path):
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory_path (str): Path to the directory
    """
    os.makedirs(directory_path, exist_ok=True)


def get_file_extension(file_path):
    """
    Get the extension of a file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: File extension (lowercase, with leading dot)
    """
    return os.path.splitext(file_path.lower())[1]


def get_file_size(file_path):
    """
    Get the size of a file in bytes.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        int: File size in bytes
    """
    return os.path.getsize(file_path)


def is_file_empty(file_path):
    """
    Check if a file is empty.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if the file is empty, False otherwise
    """
    return get_file_size(file_path) == 0


def safe_delete_file(file_path):
    """
    Safely delete a file if it exists.
    
    Args:
        file_path (str): Path to the file
    """
    if os.path.exists(file_path):
        os.unlink(file_path)


def get_base_filename(file_path):
    """
    Get the base filename without extension.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Base filename without extension
    """
    return os.path.splitext(os.path.basename(file_path))[0]
