import unittest
import cv2
import os
import sys
import time
from skimage.metrics import structural_similarity as ssim

# Add the project root to the path so we can import the slide_extractor module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from TL_slide_extractor.slide_extractor import ScreenCapture


class TestImageSimilarity(unittest.TestCase):
    """Test case for image similarity between two captures from the same monitor."""
    
    def setUp(self):
        """Set up the test environment."""
        # Ensure output directory exists
        os.makedirs("test_output", exist_ok=True)
    
    def tearDown(self):
        """Clean up after the test."""
        # Optional: Remove test files if needed
        # No cleanup needed for now
    
    def test_consecutive_captures_similarity(self):
        """Test that two consecutive captures from monitor 2 have high similarity."""
        # Capture first image
        first_image = ScreenCapture.capture_screen(screen_index=2)
        
        # Save first image for debugging
        cv2.imwrite("test_output/first_capture.png", first_image)
        
        # Short delay (not too long to avoid actual screen changes)
        time.sleep(0.5)
        
        # Capture second image
        second_image = ScreenCapture.capture_screen(screen_index=2)
        
        # Save second image for debugging
        cv2.imwrite("test_output/second_capture.png", second_image)
        
        # Convert images to grayscale for SSIM comparison
        first_gray = cv2.cvtColor(first_image, cv2.COLOR_BGR2GRAY)
        second_gray = cv2.cvtColor(second_image, cv2.COLOR_BGR2GRAY)
        
        # Calculate the Structural Similarity Index
        similarity_score, _ = ssim(first_gray, second_gray, full=True)
        
        # Print the similarity score for debugging
        print(f"Similarity score between consecutive captures: {similarity_score}")
        
        # Assert that the similarity is very high (almost identical)
        self.assertGreaterEqual(
            similarity_score, 
            0.95, 
            "Consecutive captures should have high similarity"
        )
    
    def test_identical_images(self):
        """Test that identical images have perfect similarity."""
        # Capture an image
        image = ScreenCapture.capture_screen(screen_index=2)
        
        # Calculate similarity with itself (should be 1.0)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        similarity_score, _ = ssim(image_gray, image_gray, full=True)
        
        # Assert perfect similarity
        self.assertEqual(
            similarity_score, 
            1.0, 
            "Identical images should have perfect similarity score of 1.0"
        )


if __name__ == "__main__":
    unittest.main()
