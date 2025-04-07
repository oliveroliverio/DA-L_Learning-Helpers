"""
Migration script to convert JSON learning sessions to SQLite database.
"""
import json
import os
from pathlib import Path
from database.db_manager import DatabaseManager

def migrate_json_to_sqlite(json_path=None):
    """
    Migrate data from JSON file to SQLite database
    
    Args:
        json_path: Path to the JSON file (defaults to learning-sessions.json in TL_json-friendly-markdown)
    """
    # Default JSON path if not provided
    if json_path is None:
        base_dir = Path(__file__).parent.parent
        json_path = base_dir / "TL_json-friendly-markdown" / "learning-sessions.json"
    
    # Initialize database
    db = DatabaseManager()
    db.initialize_db()
    
    # Read JSON data
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Migrate each session
        sessions = data.get('learning_sessions', [])
        for session in sessions:
            db.add_session(
                session_id=session.get('id'),
                title=session.get('title'),
                content=session.get('content')
            )
        
        print(f"Successfully migrated {len(sessions)} sessions to SQLite")
        return len(sessions)
    except Exception as e:
        print(f"Error migrating data: {e}")
        return 0

if __name__ == "__main__":
    migrate_json_to_sqlite()
