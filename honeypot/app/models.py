from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from enum import Enum


class ScamType(str, Enum):
    """Enum for different types of scams"""
    BANKING = "banking"
    UPI = "upi"
    PHISHING = "phishing"
    INVESTMENT = "investment"
    ROMANCE = "romance"
    OTHER = "other"


class ScamMessage(BaseModel):
    """Model for incoming scam message"""
    message: str
    sender_id: Optional[str] = None
    timestamp: Optional[str] = None


class DetectionResult(BaseModel):
    """Model for scam detection result"""
    is_scam: bool
    confidence: float
    scam_type: Optional[ScamType] = None
    reason: str


class ExtractedIntelligence(BaseModel):
    """Model for extracted intelligence from scam conversation"""
    bank_accounts: List[str] = []
    upi_ids: List[str] = []
    phishing_links: List[str] = []
    phone_numbers: List[str] = []
    email_addresses: List[str] = []
    suspicious_patterns: List[str] = []


class ConversationState(BaseModel):
    """Model for maintaining conversation state"""
    conversation_id: str
    messages: List[Dict[str, str]] = []
    scammer_persona: str = "elderly_person"
    extracted_intel: ExtractedIntelligence = ExtractedIntelligence()
    engagement_level: int = 0  # 0-100


class HoneypotResponse(BaseModel):
    """Model for honeypot system response"""
    conversation_id: str
    detected_scam: DetectionResult
    ai_response: str
    extracted_intelligence: ExtractedIntelligence
    conversation_state: Dict[str, Any]
