import cv2
import numpy as np
import mss
import os
import time
import threading
import queue
import pytesseract
from datetime import datetime
from skimage.metrics import structural_similarity as ssim
import re

# === Config ===


class Config:
    """Configuration settings for the application."""
    SCREEN_INDEX = 2  # 0 = all screens, since mss on macOS treats all as one virtual screen
    CAPTURE_INTERVAL = 2  # seconds between checks
    SSIM_THRESHOLD = 0.95  # lower = more sensitive to change
    OUTPUT_DIR = "captured_slides"
    OCR_QUEUE_SIZE = 100  # maximum number of images to queue for OCR processing

    @classmethod
    def initialize(cls):
        """Initialize directories based on configuration."""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)


# === Screen Capture Module ===
class ScreenCapture:
    """Handles screen capture functionality."""

    @staticmethod
    def capture_screen(screen_index=None):
        """Capture a screenshot from the specified screen index."""
        if screen_index is None:
            screen_index = Config.SCREEN_INDEX

        with mss.mss() as sct:
            monitor = sct.monitors[screen_index]
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


# === Image Processing Module ===
class ImageProcessor:
    """Handles image processing and analysis."""

    @staticmethod
    def image_similarity(img1, img2):
        """Calculate similarity between two images using SSIM."""
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        if gray1.shape != gray2.shape:
            return 0  # consider as very different

        score, _ = ssim(gray1, gray2, full=True)
        return score


# === File Management Module ===
class FileManager:
    """Handles file operations for saving and renaming images."""

    @staticmethod
    def save_image(image, output_dir=None):
        """Save an image with a timestamp filename."""
        if output_dir is None:
            output_dir = Config.OUTPUT_DIR

        timestamp = datetime.now().strftime("%y%m%d-%H%M%S")
        filepath = os.path.join(output_dir, f"{timestamp}.png")
        cv2.imwrite(filepath, image)
        print(f"[+] Slide captured: {filepath}")
        return filepath


# === OCR Module ===
class OCRProcessor:
    """Handles OCR processing of images."""

    @staticmethod
    def extract_text_from_image(image):
        """Extract text from an image using OCR with preprocessing for better results."""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply adaptive thresholding to handle different lighting conditions
            thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )

            # Noise removal using median blur
            processed = cv2.medianBlur(thresh, 3)

            # OCR with multiple language support and page segmentation mode for slide layout
            text = pytesseract.image_to_string(
                processed,
                # Page segmentation mode 1 (auto), OCR Engine mode 3 (default)
                config='--psm 1 --oem 3 -l eng'
            )

            # If text extraction fails or returns very little text, try with original image
            if not text or len(text.strip()) < 10:
                print(
                    "⚠️ Initial OCR produced limited text, trying with original image...")
                text = pytesseract.image_to_string(image)

            return text.strip()
        except Exception as e:
            print(f"❌ OCR error: {e}")
            return ""


# === Slide Capture Application ===
class SlideCapture:
    """Main application class that coordinates the slide capture process."""

    def __init__(self):
        """Initialize the slide capture application."""
        self.ocr_queue = queue.Queue(maxsize=Config.OCR_QUEUE_SIZE)
        self.last_image = None
        self.ocr_thread = None

    def start(self):
        """Start the slide capture application."""
        print("🔍 Starting slide capture...")

        # Initialize configuration
        Config.initialize()

        # Start OCR worker thread
        self.ocr_thread = threading.Thread(
            target=self._ocr_worker, daemon=True)
        self.ocr_thread.start()

        self._main_loop()

    def _main_loop(self):
        """Main loop for capturing and processing slides."""
        while True:
            current_image = ScreenCapture.capture_screen()

            if self.last_image is None:
                self._process_new_slide(current_image)
            else:
                # Check image similarity
                similarity = ImageProcessor.image_similarity(
                    current_image, self.last_image)

                if similarity < Config.SSIM_THRESHOLD:
                    print(
                        f"📝 New slide detected: similarity is {similarity:.2f}")
                    self._process_new_slide(current_image)
                else:
                    print(f"📋 Skipped: similarity is {similarity:.2f}")

            time.sleep(Config.CAPTURE_INTERVAL)

    def _process_new_slide(self, image):
        """Process a new slide image."""
        filepath = FileManager.save_image(image)
        self.last_image = image

        # Add to OCR queue for processing
        try:
            self.ocr_queue.put((filepath, image), block=False)
        except queue.Full:
            print("⚠️ OCR queue is full, skipping OCR for this image")

    def _ocr_worker(self):
        """Worker thread for OCR processing."""
        print("🔍 Starting OCR worker thread...")

        while True:
            try:
                filepath, image = self.ocr_queue.get()
                filename = os.path.basename(filepath)

                try:
                    print(f"🔤 Processing OCR for {filename}...")
                    text = OCRProcessor.extract_text_from_image(image)

                    if text:
                        # Save OCR text to file with same name + _OCR
                        base_name = os.path.splitext(filepath)[0]
                        ocr_filepath = f"{base_name}_OCR.txt"

                        with open(ocr_filepath, 'w') as f:
                            f.write(text)

                        print(f"📝 OCR text saved to {ocr_filepath}")
                    else:
                        print(f"⚠️ No text extracted from {filename}")
                except Exception as e:
                    print(f"❌ Error processing {filename}: {e}")
                finally:
                    # Always mark the task as done
                    self.ocr_queue.task_done()
            except Exception as e:
                print(f"❌ OCR worker error: {e}")
                # Continue processing even if there's an error with one image
                continue


def main():
    """Main entry point for the application."""
    app = SlideCapture()
    app.start()


if __name__ == "__main__":
    main()
