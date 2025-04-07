#!/usr/bin/env python3
"""
prep_for_json.py - Prepares markdown content for JSON storage by:
1. Escaping double quotes
2. Removing excessive blank lines (2 or more consecutive blank lines)

The script can process either a file or content from the system clipboard.
"""

import sys
import os
import re
import argparse
import subprocess
import json

def get_clipboard_content():
    """Get content from system clipboard."""
    try:
        # For macOS
        process = subprocess.Popen(
            ['pbpaste'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            print(f"Error getting clipboard content: {stderr.decode()}")
            return None
        return stdout.decode()
    except Exception as e:
        print(f"Error accessing clipboard: {e}")
        return None

def escape_double_quotes(content):
    """Escape double quotes in content for JSON compatibility."""
    # We're not using json.dumps for the entire content because we only want to
    # escape double quotes, not convert to a full JSON string with quotes around it
    return content.replace('"', '\\"')

def remove_excessive_blank_lines(content):
    """Remove excessive blank lines (2 or more consecutive blank lines)."""
    # Replace 3 or more newlines with 2 newlines
    return re.sub(r'\n{3,}', '\n\n', content)

def sanitize_markdown(content):
    """Sanitize markdown content for JSON compatibility."""
    content = escape_double_quotes(content)
    content = remove_excessive_blank_lines(content)
    return content

def save_content(content, input_path=None):
    """Save the sanitized content to a file."""
    if input_path:
        # For file input, append _esc_dblqts to the original filename
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_esc_dblqts{ext}"
    else:
        # For clipboard input
        output_path = "system_clipboard_esc_dblqts.md"
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Sanitized content saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error saving file: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Prepare markdown content for JSON by escaping double quotes and removing excessive blank lines.')
    parser.add_argument('-f', '--file', help='Path to markdown file to process')
    parser.add_argument('-t', '--test', action='store_true', 
                        help='Test the sanitized content by loading it as JSON')
    args = parser.parse_args()

    # Get content from file or clipboard
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"Processing file: {args.file}")
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    else:
        content = get_clipboard_content()
        if not content:
            print("No content found in clipboard.")
            return
        print("Processing content from clipboard.")

    # Sanitize the content
    sanitized_content = sanitize_markdown(content)
    
    # Save the sanitized content
    output_path = save_content(sanitized_content, args.file)
    
    # Test JSON compatibility if requested
    if args.test and output_path:
        try:
            # Create a simple JSON object with the content
            test_json = json.dumps({"content": sanitized_content})
            # Try to parse it back
            json.loads(test_json)
            print("✅ Content is JSON compatible.")
        except json.JSONDecodeError as e:
            print(f"❌ Content is NOT JSON compatible: {e}")

if __name__ == "__main__":
    main()
