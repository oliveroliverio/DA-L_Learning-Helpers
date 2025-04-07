"""
Unit tests for the database manager.
"""
import unittest
import os
import sys
from pathlib import Path

# Add parent directory to path to import database module
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager"""
    
    def setUp(self):
        """Set up test database"""
        # Use in-memory database for testing
        self.db = DatabaseManager()
        # Override db_path to use in-memory database
        self.db.db_path = ":memory:"
        self.db.connect()
        self.db.initialize_db()
    
    def tearDown(self):
        """Clean up after tests"""
        self.db.close()
    
    def test_add_and_get_session(self):
        """Test adding and retrieving a session"""
        # Add a test session
        session_id = "test-123"
        title = "Test Session"
        content = "This is test content"
        
        self.db.add_session(session_id, title, content)
        
        # Retrieve the session
        session = self.db.get_session(session_id)
        
        # Assert session was retrieved correctly
        self.assertIsNotNone(session)
        self.assertEqual(session['id'], session_id)
        self.assertEqual(session['title'], title)
        self.assertEqual(session['content'], content)
    
    def test_update_session(self):
        """Test updating a session"""
        # Add a test session
        session_id = "test-456"
        title = "Original Title"
        content = "Original content"
        
        self.db.add_session(session_id, title, content)
        
        # Update the session
        new_title = "Updated Title"
        new_content = "Updated content"
        self.db.update_session(session_id, title=new_title, content=new_content)
        
        # Retrieve the updated session
        session = self.db.get_session(session_id)
        
        # Assert session was updated correctly
        self.assertEqual(session['title'], new_title)
        self.assertEqual(session['content'], new_content)
    
    def test_delete_session(self):
        """Test deleting a session"""
        # Add a test session
        session_id = "test-789"
        title = "Delete Test"
        content = "Content to delete"
        
        self.db.add_session(session_id, title, content)
        
        # Delete the session
        self.db.delete_session(session_id)
        
        # Try to retrieve the deleted session
        session = self.db.get_session(session_id)
        
        # Assert session was deleted
        self.assertIsNone(session)
    
    def test_get_all_sessions(self):
        """Test retrieving all sessions"""
        # Add multiple test sessions
        sessions = [
            ("test-a", "Session A", "Content A"),
            ("test-b", "Session B", "Content B"),
            ("test-c", "Session C", "Content C")
        ]
        
        for session_id, title, content in sessions:
            self.db.add_session(session_id, title, content)
        
        # Retrieve all sessions
        all_sessions = self.db.get_all_sessions()
        
        # Assert all sessions were retrieved
        self.assertEqual(len(all_sessions), len(sessions))
    
    def test_search_sessions(self):
        """Test searching for sessions"""
        # Add test sessions with different content
        self.db.add_session("test-search-1", "Python Learning", "Content about Python")
        self.db.add_session("test-search-2", "JavaScript Notes", "Content about JS")
        self.db.add_session("test-search-3", "More Python", "Advanced Python topics")
        
        # Search for Python sessions
        python_sessions = self.db.search_sessions("Python")
        
        # Assert correct sessions were found
        self.assertEqual(len(python_sessions), 2)
        
        # Search for JavaScript sessions
        js_sessions = self.db.search_sessions("JavaScript")
        
        # Assert correct sessions were found
        self.assertEqual(len(js_sessions), 1)

if __name__ == "__main__":
    unittest.main()
