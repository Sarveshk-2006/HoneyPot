import re
from typing import Tuple
from app.models import DetectionResult, ScamType


class ScamDetector:
    """Service to detect scam messages using pattern matching and keyword analysis"""
    
    # Common scam keywords
    SCAM_KEYWORDS = {
        'banking': [
            'verify account', 'update bank', 'confirm identity', 'enter password',
            'account locked', 'unusual activity', 'click link', 'verify credentials',
            'immediate action', 'bank details', 'swift code', 'account number'
        ],
        'upi': [
            'upi payment', 'send money', 'upi id', 'upi transfer', 'receive money',
            'quick payment', 'instant transfer', 'upi rupees'
        ],
        'phishing': [
            'click here', 'verify now', 'confirm details', 'update information',
            'suspicious activity', 'urgent action', 'act now', 'limited time'
        ],
        'investment': [
            'guaranteed returns', 'high profit', 'quick money', 'invest now',
            'limited offer', 'risk-free', 'double your money', 'easy money',
            'passive income', 'work from home'
        ],
        'romance': [
            'fall in love', 'marry me', 'send money', 'help me', 'financial help',
            'emergency', 'medical bills', 'surgery', 'visa application'
        ]
    }
    
    # URL patterns
    URL_PATTERN = r'https?://[^\s]+'
    
    # Bank account pattern (simplified)
    ACCOUNT_PATTERN = r'\b\d{10,18}\b'
    
    # UPI ID pattern
    UPI_PATTERN = r'[\w\.-]+@[a-zA-Z]{3,}'
    
    @staticmethod
    def detect_scam(message: str) -> DetectionResult:
        """
        Detect if a message is a scam attempt
        
        Args:
            message: The message to analyze
            
        Returns:
            DetectionResult with scam status, confidence, and type
        """
        message_lower = message.lower()
        
        # Score for each scam type
        scores = {scam_type: 0 for scam_type in ScamType}
        
        # Check keywords
        for scam_type, keywords in ScamDetector.SCAM_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    scores[scam_type] += 1
        
        # Check for URLs/links (phishing indicator)
        if re.search(ScamDetector.URL_PATTERN, message):
            scores['phishing'] += 2
        
        # Check for urgency patterns
        urgency_patterns = [
            r'\b(urgent|immediate|hurry|quick|now|asap|today)\b',
            r'(!!!|!!!)',
            r'\b(act now|verify now|click now)\b'
        ]
        for pattern in urgency_patterns:
            if re.search(pattern, message_lower):
                scores['phishing'] += 1
        
        # Check for personal info requests
        info_patterns = [
            r'\b(password|otp|pin|cvv|ssn|account number|routing number)\b',
            r'\b(confirm|verify|provide|send)\b.*\b(password|otp|pin|cvv)\b'
        ]
        for pattern in info_patterns:
            if re.search(pattern, message_lower):
                scores['phishing'] += 2
        
        # Find dominant scam type
        max_score = max(scores.values())
        if max_score == 0:
            return DetectionResult(
                is_scam=False,
                confidence=0.0,
                scam_type=None,
                reason="No scam indicators detected"
            )
        
        detected_type = max(scores, key=scores.get)
        confidence = min(max_score / 10, 1.0)  # Normalize confidence
        
        # Determine if it's actually a scam based on threshold
        is_scam = confidence >= 0.2  # Lower threshold for detection (URLs are suspicious enough at 0.2)
        
        return DetectionResult(
            is_scam=is_scam,
            confidence=confidence,
            scam_type=ScamType(detected_type) if is_scam else None,
            reason=f"Detected {detected_type} scam with {scores[detected_type]} indicators"
        )
    
    @staticmethod
    def extract_urls(message: str) -> list:
        """Extract URLs from message"""
        return re.findall(ScamDetector.URL_PATTERN, message)
    
    @staticmethod
    def extract_accounts(message: str) -> list:
        """Extract potential account numbers"""
        return re.findall(ScamDetector.ACCOUNT_PATTERN, message)
    
    @staticmethod
    def extract_upi_ids(message: str) -> list:
        """Extract UPI IDs from message"""
        return re.findall(ScamDetector.UPI_PATTERN, message)
