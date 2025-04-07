"""
SQLAlchemy models for learning sessions database.
This is optional if you prefer using the ORM approach instead of raw SQL.
"""
from sqlalchemy import Column, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pathlib import Path

# Create base class for declarative models
Base = declarative_base()

class LearningSession(Base):
    """SQLAlchemy model for learning sessions"""
    __tablename__ = 'learning_sessions'
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<LearningSession(id='{self.id}', title='{self.title}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# Database connection setup
def get_engine():
    """Create SQLAlchemy engine"""
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    db_path = data_dir / "learning_sessions.db"
    return create_engine(f"sqlite:///{db_path}")

def get_session():
    """Create a new SQLAlchemy session"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def init_db():
    """Initialize database and create tables"""
    engine = get_engine()
    Base.metadata.create_all(engine)
