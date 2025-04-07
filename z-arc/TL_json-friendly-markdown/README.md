# JSON-Friendly Markdown Converter

A GUI tool that converts raw markdown to JSON-friendly format by escaping double quotes and optionally converting newlines to `\n` literals.

## Features

- Two-panel interface with raw markdown on the left and processed markdown on the right
- Drag and drop markdown files directly into the application
- Automatic processing as you type or paste content
- Option to convert newlines to `\n` literals for direct JSON pasting
- Copy button to easily copy the processed markdown to clipboard
- Clear button to reset the input

## Usage

1. Run the application:
   ```bash
   python json_markdown_gui.py
   ```

2. Input your markdown by either:
   - Pasting directly into the left panel
   - Dragging and dropping a markdown file

3. The JSON-friendly markdown will automatically appear in the right panel

4. Toggle the "Convert Newlines to \n" option if you need newlines as literal `\n` characters

5. Click "Copy JSON-Friendly Markdown" to copy the processed text to your clipboard

6. Paste the processed markdown into your JSON file

## Requirements

- Python 3.6+
- PyQt5

## Installation

```bash
uv venv && source .venv/bin/activate && uv add PyQt5
```

## How It Works

The application uses the `prep_for_json.py` script to:

1. Escape double quotes (`"` → `\"`)
2. Remove excessive blank lines (3+ consecutive blank lines → 2 blank lines)
3. Optionally convert newlines to the literal string `\n`

This makes the markdown content safe to use as a string value in JSON files.
