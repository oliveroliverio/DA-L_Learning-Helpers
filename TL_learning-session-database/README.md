# Learning Session Database

A SQLite database implementation for storing and managing learning sessions with markdown content.

## Features

- Store large markdown content efficiently in a SQLite database
- Simple API for adding, retrieving, updating, and deleting learning sessions
- Search functionality to find sessions by title or content
- Migration tool to convert existing JSON data to SQLite
- Support for both raw SQL and SQLAlchemy ORM approaches

## Project Structure

```
TL_learning-session-database/
├── database/
│   ├── __init__.py
│   ├── db_manager.py     # Core database operations using SQLite
│   ├── models.py         # SQLAlchemy models (optional ORM approach)
│   └── migrations/       # For schema changes
│       └── __init__.py
├── data/
│   └── learning_sessions.db  # SQLite database file (created on first run)
├── tests/
│   └── test_db.py        # Database unit tests
├── json_to_sqlite.py     # Migration script for JSON to SQLite
└── README.md             # This file
```

## Usage

### Basic Usage with DatabaseManager

```python
from database.db_manager import DatabaseManager

# Initialize the database
db = DatabaseManager()
db.initialize_db()

# Add a new learning session
db.add_session(
    session_id="260406-1",
    title="ChatGPT Convo 260406",
    content="# ChatGPT Conversation\n\n**ChatGPT:**\n\nhelp me build a MacOS application..."
)

# Retrieve a session
session = db.get_session("260406-1")
print(session['title'])  # "ChatGPT Convo 260406"

# Get all sessions (without content for efficiency)
all_sessions = db.get_all_sessions()
for session in all_sessions:
    print(f"{session['id']}: {session['title']}")

# Update a session
db.update_session("260406-1", title="Updated Title")

# Delete a session
db.delete_session("260406-1")

# Search for sessions
results = db.search_sessions("MacOS")
```

### Using SQLAlchemy ORM (Optional)

```python
from database.models import init_db, get_session, LearningSession

# Initialize the database
init_db()

# Create a session
db_session = get_session()

# Add a new learning session
new_session = LearningSession(
    id="260406-2",
    title="Another ChatGPT Convo",
    content="# Another Conversation\n\nThis is the content..."
)
db_session.add(new_session)
db_session.commit()

# Query sessions
sessions = db_session.query(LearningSession).all()
for session in sessions:
    print(session.title)

# Close the session when done
db_session.close()
```

### Migrating from JSON

To migrate existing learning sessions from a JSON file:

```bash
python json_to_sqlite.py
```

By default, this will look for the JSON file at `../TL_json-friendly-markdown/learning-sessions.json`. You can specify a different path by modifying the script.

## Requirements

- Python 3.6+
- SQLite3 (included with Python)
- SQLAlchemy (optional, for ORM support)

## Installation

```bash
# Create and activate virtual environment
uv venv && source .venv/bin/activate

# Install dependencies
uv add sqlalchemy
```

## Testing

Run the unit tests to verify database functionality:

```bash
python -m unittest tests/test_db.py
```
