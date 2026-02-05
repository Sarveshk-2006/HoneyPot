import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration settings for the honeypot system"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Mock Scammer API
    MOCK_SCAMMER_API_URL = os.getenv("MOCK_SCAMMER_API_URL", "http://localhost:8001")
    MOCK_SCAMMER_API_KEY = os.getenv("MOCK_SCAMMER_API_KEY", "")
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    
    # Honeypot Configuration
    MAX_CONVERSATION_LENGTH = 20  # Max messages before auto-terminate
    SCAM_DETECTION_THRESHOLD = 0.6
    EXTRACTION_TIMEOUT = 30  # seconds
    
    # Personas for engagement
    SCAMMER_PERSONAS = {
        "elderly_person": "I'm an elderly person who might be vulnerable",
        "curious_user": "I'm a curious user interested in offers",
        "desperate_person": "I'm desperate for money and willing to take risks",
    }
