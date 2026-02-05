# Agentic Honeypot for Scam Detection & Intelligence Extraction

## Overview
An autonomous AI honeypot system that detects scam messages and actively engages scammers using believable personas to extract sensitive information like bank account details, UPI IDs, and phishing links.

## Project Structure

```
honeypot/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration settings
│   ├── models.py              # Pydantic models
│   ├── agents/
│   │   ├── __init__.py
│   │   └── engagement_agent.py # AI engagement logic
│   └── services/
│       ├── __init__.py
│       ├── detector.py         # Scam detection service
│       ├── extractor.py        # Intelligence extraction
│       └── mock_scammer_api.py # Mock API client
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## Features

1. **Scam Detection**: Identifies scam messages using pattern matching and keyword analysis
2. **Intelligent Engagement**: Uses AI personas to interact convincingly with scammers
3. **Intelligence Extraction**: Extracts bank accounts, UPI IDs, phishing links, and phone numbers
4. **Conversation Management**: Maintains conversation history and engagement levels
5. **JSON Response Format**: Structured output for easy integration

## Installation

1. Clone the repository:
```bash
cd honeypot
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## API Endpoints

### 1. Health Check
```
GET /health
```

### 2. Analyze Message
```
POST /analyze
Content-Type: application/json

{
  "message": "Hello, I'm a Nigerian prince and I need your help...",
  "sender_id": "optional_sender_id",
  "timestamp": "2024-02-05T10:30:00"
}
```

Response:
```json
{
  "conversation_id": "uuid",
  "detected_scam": {
    "is_scam": true,
    "confidence": 0.85,
    "scam_type": "banking",
    "reason": "Detected banking scam with multiple indicators"
  },
  "ai_response": "I can provide my bank details. What information do you need?",
  "extracted_intelligence": {
    "bank_accounts": [],
    "upi_ids": [],
    "phishing_links": [],
    "phone_numbers": [],
    "email_addresses": [],
    "suspicious_patterns": []
  },
  "conversation_state": {
    "conversation_id": "uuid",
    "engagement_level": 10,
    "message_count": 1,
    "is_active": true
  }
}
```

### 3. Continue Conversation
```
POST /conversation/{conversation_id}
Content-Type: application/json

{
  "message": "Here's my bank account number: 1234567890"
}
```

### 4. Get Conversation
```
GET /conversation/{conversation_id}
```

### 5. Terminate Conversation
```
POST /terminate/{conversation_id}
```

### 6. Get Statistics
```
GET /stats
```

## Scam Detection Patterns

The system detects:
- **Banking Scams**: Account verification, password requests
- **UPI Scams**: Payment requests, UPI ID extraction
- **Phishing**: Malicious links, credential requests
- **Investment**: Guaranteed returns, quick money
- **Romance**: Love scams, financial emergencies

## Intelligence Extraction

Extracts:
- Bank account numbers (10-18 digits)
- UPI IDs (format: user@bank)
- Phishing links (http/https)
- Phone numbers (various formats)
- Email addresses
- Suspicious patterns

## Configuration

Edit `app/config.py` for:
- OpenAI API key
- Mock Scammer API endpoint
- Maximum conversation length
- Detection threshold
- Engagement personas

## Development

```bash
# Run tests
pytest tests/

# Check code style
flake8 app/

# Format code
black app/
```

## Deployment

For production deployment:

1. Set `DEBUG=false` in `.env`
2. Use production ASGI server:
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -b 0.0.0.0:8000
```

3. Set up reverse proxy (nginx/Apache)
4. Use HTTPS/SSL certificates
5. Implement rate limiting
6. Add authentication for API endpoints

## Testing the Honeypot

### Example Scam Message
```json
{
  "message": "Hello, your bank account has been flagged. Click here to verify: http://phishing-link.com. Please enter your password: ****"
}
```

## Future Enhancements

- [ ] Integration with real LLM APIs (OpenAI, Claude)
- [ ] Multi-language support
- [ ] Advanced persona customization
- [ ] Real-time analytics dashboard
- [ ] Database storage for conversations
- [ ] Email/SMS integration
- [ ] Machine learning for pattern detection
- [ ] Webhook notifications

## License
MIT License

## Contact
[Your contact information]
