import pytest
from fastapi.testclient import TestClient
from app.main import app, detector, extractor
from app.models import ScamMessage, ScamType

client = TestClient(app)


class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestScamDetection:
    """Test scam detection functionality"""
    
    def test_banking_scam_detection(self):
        """Test banking scam detection"""
        message = ScamMessage(message="Verify your account now. Click here to confirm your password.")
        response = client.post("/analyze", json=message.model_dump())
        
        assert response.status_code == 200
        data = response.json()
        assert data["detected_scam"]["is_scam"] == True
    
    def test_phishing_scam_detection(self):
        """Test phishing scam detection"""
        message = ScamMessage(message="Click https://verify-bank.com to update your details")
        response = client.post("/analyze", json=message.model_dump())
        
        assert response.status_code == 200
        data = response.json()
        assert data["detected_scam"]["is_scam"] == True
    
    def test_legit_message(self):
        """Test legitimate message"""
        message = ScamMessage(message="Hi, how are you doing today?")
        response = client.post("/analyze", json=message.model_dump())
        
        assert response.status_code == 200
        data = response.json()
        assert data["detected_scam"]["is_scam"] == False


class TestIntelligenceExtraction:
    """Test intelligence extraction"""
    
    def test_extract_urls(self):
        """Test URL extraction"""
        message = "Click on https://malicious-link.com for verification"
        urls = detector.extract_urls(message)
        assert len(urls) > 0
        assert "https://malicious-link.com" in urls
    
    def test_extract_account_numbers(self):
        """Test account number extraction"""
        message = "My account number is 1234567890"
        accounts = detector.extract_accounts(message)
        assert "1234567890" in accounts
    
    def test_extract_upi_ids(self):
        """Test UPI ID extraction"""
        message = "Send money to user@okhdfcbank"
        upi_ids = detector.extract_upi_ids(message)
        assert len(upi_ids) > 0


class TestConversationFlow:
    """Test conversation flow"""
    
    def test_create_conversation(self):
        """Test creating a new conversation"""
        message = ScamMessage(message="Hello, verify your bank account")
        response = client.post("/analyze", json=message.model_dump())
        
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert "ai_response" in data
    
    def test_continue_conversation(self):
        """Test continuing a conversation"""
        # First message
        message1 = ScamMessage(message="Verify account number")
        response1 = client.post("/analyze", json=message1.model_dump())
        conversation_id = response1.json()["conversation_id"]
        
        # Continue conversation
        message2 = ScamMessage(message="Here's my account: 1234567890")
        response2 = client.post(f"/conversation/{conversation_id}", json=message2.model_dump())
        
        assert response2.status_code == 200
        data = response2.json()
        assert data["conversation_id"] == conversation_id


class TestStatistics:
    """Test statistics endpoint"""
    
    def test_get_stats(self):
        """Test getting honeypot statistics"""
        response = client.get("/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "active_conversations" in data
        assert "total_messages" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
