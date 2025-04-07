"""
Database manager for learning sessions SQLite database.
Handles connections, queries, and CRUD operations.
"""
import os
import sqlite3
from pathlib import Path
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        # Create data directory if it doesn't exist
        data_dir = Path(__file__).parent.parent / "data"
        data_dir.mkdir(exist_ok=True)
        
        # Database path
        self.db_path = data_dir / "learning_sessions.db"
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connect to the SQLite database"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.cursor = self.conn.cursor()
        return self.conn
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
    
    def initialize_db(self):
        """Create tables if they don't exist"""
        self.connect()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_sessions (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()
        self.close()
    
    def add_session(self, session_id, title, content):
        """Add a new learning session"""
        self.connect()
        self.cursor.execute(
            "INSERT INTO learning_sessions (id, title, content) VALUES (?, ?, ?)",
            (session_id, title, content)
        )
        self.conn.commit()
        self.close()
    
    def get_session(self, session_id):
        """Get a learning session by ID"""
        self.connect()
        self.cursor.execute("SELECT * FROM learning_sessions WHERE id = ?", (session_id,))
        result = self.cursor.fetchone()
        result_dict = dict(result) if result else None
        self.close()
        return result_dict
    
    def get_all_sessions(self):
        """Get all learning sessions"""
        self.connect()
        self.cursor.execute("SELECT id, title, created_at FROM learning_sessions ORDER BY created_at DESC")
        results = [dict(row) for row in self.cursor.fetchall()]
        self.close()
        return results
    
    def update_session(self, session_id, title=None, content=None):
        """Update an existing learning session"""
        self.connect()
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        
        if content is not None:
            updates.append("content = ?")
            params.append(content)
        
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE learning_sessions SET {', '.join(updates)} WHERE id = ?"
            params.append(session_id)
            self.cursor.execute(query, params)
            self.conn.commit()
        
        self.close()
        
    def delete_session(self, session_id):
        """Delete a learning session by ID"""
        self.connect()
        self.cursor.execute("DELETE FROM learning_sessions WHERE id = ?", (session_id,))
        self.conn.commit()
        self.close()
    
    def search_sessions(self, search_term):
        """Search for learning sessions by title or content"""
        self.connect()
        search_pattern = f"%{search_term}%"
        self.cursor.execute(
            "SELECT id, title, created_at FROM learning_sessions WHERE title LIKE ? OR content LIKE ? ORDER BY created_at DESC",
            (search_pattern, search_pattern)
        )
        results = [dict(row) for row in self.cursor.fetchall()]
        self.close()
        return results
