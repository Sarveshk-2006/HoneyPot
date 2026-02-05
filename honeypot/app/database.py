"""
Database Models for Agentic Honeypot
Enables persistent storage of conversations and intelligence
"""

from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./honeypot.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ConversationRecord(Base):
    """Database model for storing conversation data"""
    __tablename__ = "conversations"
    
    conversation_id = Column(String, primary_key=True, index=True)
    sender_id = Column(String, nullable=True, index=True)
    scam_type = Column(String, nullable=True)
    confidence = Column(Float, default=0.0)
    engagement_level = Column(Integer, default=0)
    persona_used = Column(String, default="elderly_person")
    
    # Extracted intelligence
    bank_accounts = Column(JSON, default=list)
    upi_ids = Column(JSON, default=list)
    phishing_links = Column(JSON, default=list)
    phone_numbers = Column(JSON, default=list)
    email_addresses = Column(JSON, default=list)
    suspicious_patterns = Column(JSON, default=list)
    
    # Conversation metadata
    total_messages = Column(Integer, default=0)
    conversation_text = Column(Text, nullable=True)  # Full conversation
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ConversationRecord {self.conversation_id}>"


class IntelligenceRecord(Base):
    """Database model for storing extracted intelligence"""
    __tablename__ = "intelligence"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, index=True)
    intelligence_type = Column(String)  # 'bank_account', 'upi_id', 'phishing_link', etc.
    value = Column(String, unique=True)
    confidence = Column(Float, default=1.0)
    
    found_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<IntelligenceRecord {self.intelligence_type}: {self.value}>"


class ScamPatternRecord(Base):
    """Database model for tracking scam patterns"""
    __tablename__ = "scam_patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    scam_type = Column(String, index=True)
    pattern = Column(String)
    occurrence_count = Column(Integer, default=1)
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    confidence_average = Column(Float, default=0.5)
    
    def __repr__(self):
        return f"<ScamPatternRecord {self.scam_type}: {self.pattern}>"


# Create all tables
Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database utility functions

def save_conversation(conversation_id: str, conv_data: dict, db=None):
    """Save conversation to database"""
    if db is None:
        db = SessionLocal()
    
    try:
        record = ConversationRecord(
            conversation_id=conversation_id,
            **conv_data
        )
        db.add(record)
        db.commit()
        return record
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_conversation_record(conversation_id: str, db=None):
    """Retrieve conversation from database"""
    if db is None:
        db = SessionLocal()
    
    try:
        return db.query(ConversationRecord).filter(
            ConversationRecord.conversation_id == conversation_id
        ).first()
    finally:
        db.close()


def save_intelligence(conversation_id: str, intelligence_type: str, value: str, db=None):
    """Save extracted intelligence to database"""
    if db is None:
        db = SessionLocal()
    
    try:
        # Check if already exists
        existing = db.query(IntelligenceRecord).filter(
            IntelligenceRecord.value == value
        ).first()
        
        if not existing:
            record = IntelligenceRecord(
                conversation_id=conversation_id,
                intelligence_type=intelligence_type,
                value=value
            )
            db.add(record)
            db.commit()
            return record
        return existing
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
