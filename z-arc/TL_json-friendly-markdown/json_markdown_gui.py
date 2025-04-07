#!/usr/bin/env python3
"""
JSON-Friendly Markdown GUI

A GUI application that allows users to:
1. Paste raw markdown or drag-drop markdown files
2. Automatically convert the markdown to JSON-friendly format
3. Copy the processed markdown to clipboard for use in JSON files
"""

import sys
import os
import re
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTextEdit, QPushButton, QLabel, 
                            QFileDialog, QMessageBox, QSplitter)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent

# Import functions from prep_for_json.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from prep_for_json import escape_double_quotes, remove_excessive_blank_lines

class MarkdownTextEdit(QTextEdit):
    """Custom QTextEdit that accepts drag and drop of markdown files."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events for files."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)
            
    def dropEvent(self, event: QDropEvent):
        """Handle drop events for files."""
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith(('.md', '.markdown', '.txt')):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.setText(f.read())
                        self.parent().parent().process_markdown()  # Call the process function
                        return
                    except Exception as e:
                        QMessageBox.warning(self, "Error", f"Could not read file: {e}")
        super().dropEvent(event)

class JSONMarkdownGUI(QMainWindow):
    """Main window for the JSON-Friendly Markdown GUI application."""
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle("JSON-Friendly Markdown Converter")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create splitter for the two panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel (raw markdown)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        left_label = QLabel("Raw Markdown (paste here or drag-drop a file)")
        left_label.setFont(QFont("Arial", 12, QFont.Bold))
        left_layout.addWidget(left_label)
        
        self.raw_markdown = MarkdownTextEdit()
        self.raw_markdown.setFont(QFont("Courier New", 11))
        self.raw_markdown.setPlaceholderText("Paste your markdown here or drag and drop a markdown file...")
        self.raw_markdown.textChanged.connect(self.process_markdown)
        left_layout.addWidget(self.raw_markdown)
        
        # Add clear button for raw markdown
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_raw_markdown)
        left_layout.addWidget(clear_button)
        
        splitter.addWidget(left_widget)
        
        # Right panel (JSON-friendly markdown)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        right_label = QLabel("JSON-Friendly Markdown")
        right_label.setFont(QFont("Arial", 12, QFont.Bold))
        right_layout.addWidget(right_label)
        
        self.json_markdown = QTextEdit()
        self.json_markdown.setFont(QFont("Courier New", 11))
        self.json_markdown.setReadOnly(True)
        self.json_markdown.setPlaceholderText("JSON-friendly markdown will appear here...")
        right_layout.addWidget(self.json_markdown)
        
        # Add copy button for JSON-friendly markdown
        copy_button = QPushButton("Copy JSON-Friendly Markdown")
        copy_button.clicked.connect(self.copy_json_markdown)
        right_layout.addWidget(copy_button)
        
        # Add option for newline conversion
        self.newline_layout = QHBoxLayout()
        self.newline_checkbox = QPushButton("Convert Newlines to \\n")
        self.newline_checkbox.setCheckable(True)
        self.newline_checkbox.toggled.connect(self.process_markdown)
        self.newline_layout.addWidget(self.newline_checkbox)
        
        # Add process button
        process_button = QPushButton("Process Markdown")
        process_button.clicked.connect(self.process_markdown)
        self.newline_layout.addWidget(process_button)
        
        right_layout.addLayout(self.newline_layout)
        
        splitter.addWidget(right_widget)
        
        # Set initial splitter sizes
        splitter.setSizes([600, 600])
        
        self.statusBar().showMessage("Ready")
        self.show()
    
    def process_markdown(self):
        """Process the raw markdown and update the JSON-friendly markdown."""
        raw_text = self.raw_markdown.toPlainText()
        if not raw_text:
            self.json_markdown.clear()
            return
        
        try:
            # Sanitize the markdown
            processed_text = escape_double_quotes(raw_text)
            processed_text = remove_excessive_blank_lines(processed_text)
            
            # Convert newlines to \n if the option is checked
            if self.newline_checkbox.isChecked():
                processed_text = processed_text.replace('\n', '\\n')
            
            # Update the JSON-friendly markdown
            self.json_markdown.setText(processed_text)
            self.statusBar().showMessage("Markdown processed successfully")
        except Exception as e:
            self.statusBar().showMessage(f"Error processing markdown: {e}")
    
    def copy_json_markdown(self):
        """Copy the JSON-friendly markdown to the clipboard."""
        text = self.json_markdown.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.statusBar().showMessage("JSON-friendly markdown copied to clipboard")
        else:
            self.statusBar().showMessage("No JSON-friendly markdown to copy")
    
    def clear_raw_markdown(self):
        """Clear the raw markdown text edit."""
        self.raw_markdown.clear()
        self.statusBar().showMessage("Raw markdown cleared")

def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    gui = JSONMarkdownGUI()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
