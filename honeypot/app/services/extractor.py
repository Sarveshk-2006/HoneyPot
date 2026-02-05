import re
from typing import List
from app.models import ExtractedIntelligence


class IntelligenceExtractor:
    """Service to extract sensitive information from scam messages"""
    
    # Pattern definitions
    PATTERNS = {
        'bank_accounts': [
            r'\b\d{10,18}\b',  # Generic account numbers
            r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b',  # Formatted account
        ],
        'upi_ids': [
            r'[\w\.-]+@(okhdfcbank|okaxis|okicici|okSBI|oksyndicate|okbob|okpnb|ybl|payworld|upi)\b',
            r'[\w\.-]+@[a-z]+',  # Generic UPI pattern
        ],
        'phishing_links': [
            r'https?://[^\s]+',
            r'www\.[^\s]+',
            r'bit\.ly/\w+',
            r'tinyurl\.com/\w+',
        ],
        'phone_numbers': [
            r'\+\d{1,3}\s?\d{1,14}',  # International format
            r'\b\d{10}\b',  # Indian 10-digit
            r'\+91[\s\-]?\d{5}[\s\-]?\d{5}',  # Indian with country code
        ],
        'email_addresses': [
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        ],
    }
    
    # Suspicious patterns that might indicate scam
    SUSPICIOUS_PATTERNS = [
        r'\b(verify|confirm|update).*\b(account|password|otp|cvv)\b',
        r'\b(urgent|immediate|asap|act now)\b',
        r'\b(limited|offer|guaranteed|risk-free)\b',
        r'\b(click|visit|open|login)\b.*\b(link|url|site)\b',
        r'\b(send|transfer|wire|pay).*\b(money|rupees|amount)\b.*\b(immediately|now|urgent)\b',
    ]
    
    @staticmethod
    def extract_intelligence(message: str, conversation_history: List[str] = None) -> ExtractedIntelligence:
        """
        Extract intelligence from scam message
        
        Args:
            message: Message to extract from
            conversation_history: Previous messages in conversation
            
        Returns:
            ExtractedIntelligence object with extracted details
        """
        intelligence = ExtractedIntelligence()
        
        # Combine message with history for better context
        full_text = message
        if conversation_history:
            full_text = " ".join(conversation_history) + " " + message
        
        # Extract each type of information
        intelligence.bank_accounts = IntelligenceExtractor._extract_pattern(
            full_text, IntelligenceExtractor.PATTERNS['bank_accounts']
        )
        
        intelligence.upi_ids = IntelligenceExtractor._extract_pattern(
            full_text, IntelligenceExtractor.PATTERNS['upi_ids']
        )
        
        intelligence.phishing_links = IntelligenceExtractor._extract_pattern(
            full_text, IntelligenceExtractor.PATTERNS['phishing_links']
        )
        
        intelligence.phone_numbers = IntelligenceExtractor._extract_pattern(
            full_text, IntelligenceExtractor.PATTERNS['phone_numbers']
        )
        
        intelligence.email_addresses = IntelligenceExtractor._extract_pattern(
            full_text, IntelligenceExtractor.PATTERNS['email_addresses']
        )
        
        # Extract suspicious patterns
        intelligence.suspicious_patterns = [
            pattern for pattern in IntelligenceExtractor.SUSPICIOUS_PATTERNS
            if re.search(pattern, full_text, re.IGNORECASE)
        ]
        
        return intelligence
    
    @staticmethod
    def _extract_pattern(text: str, patterns: List[str]) -> List[str]:
        """
        Extract matches from text using multiple regex patterns
        
        Args:
            text: Text to search in
            patterns: List of regex patterns
            
        Returns:
            List of unique matches
        """
        matches = set()
        for pattern in patterns:
            try:
                found = re.findall(pattern, text, re.IGNORECASE)
                matches.update(found)
            except re.error:
                pass
        return list(matches)
