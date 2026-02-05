# Agentic Honeypot - API Documentation

## Quick Start

Server running at: `http://127.0.0.1:8000`

### Interactive API Documentation
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## Endpoints

### 1. Health Check
```bash
curl -X GET http://127.0.0.1:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Agentic Honeypot"
}
```

---

### 2. Analyze Scam Message (First Message)

**Endpoint:** `POST /analyze`

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! Your bank account has been flagged. Click here: http://fake-bank.com",
    "sender_id": "user123",
    "timestamp": "2024-02-05T10:30:00"
  }'
```

**Response:**
```json
{
  "conversation_id": "663434ef-1314-4857-ae3a-e05ac8e1bdce",
  "detected_scam": {
    "is_scam": true,
    "confidence": 0.7,
    "scam_type": "phishing",
    "reason": "Detected phishing scam with 7 indicators"
  },
  "ai_response": "I can provide my bank details. What information do you need?",
  "extracted_intelligence": {
    "bank_accounts": [],
    "upi_ids": [],
    "phishing_links": ["http://fake-bank.com"],
    "phone_numbers": [],
    "email_addresses": [],
    "suspicious_patterns": ["verify|confirm|update.*account|password|otp"]
  },
  "conversation_state": {
    "conversation_id": "663434ef-1314-4857-ae3a-e05ac8e1bdce",
    "engagement_level": 10,
    "message_count": 1,
    "is_active": true
  }
}
```

---

### 3. Continue Conversation

**Endpoint:** `POST /conversation/{conversation_id}`

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/conversation/663434ef-1314-4857-ae3a-e05ac8e1bdce \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Here is my bank account: 1234567890"
  }'
```

**Response:**
```json
{
  "conversation_id": "663434ef-1314-4857-ae3a-e05ac8e1bdce",
  "detected_scam": {
    "is_scam": true,
    "confidence": 0.65,
    "scam_type": "banking",
    "reason": "Detected banking scam with 6 indicators"
  },
  "ai_response": "Thank you for providing that information. What should I do next?",
  "extracted_intelligence": {
    "bank_accounts": ["1234567890"],
    "upi_ids": [],
    "phishing_links": [],
    "phone_numbers": [],
    "email_addresses": [],
    "suspicious_patterns": []
  },
  "conversation_state": {
    "conversation_id": "663434ef-1314-4857-ae3a-e05ac8e1bdce",
    "engagement_level": 20,
    "message_count": 2,
    "is_active": true
  }
}
```

---

### 4. Get Conversation Details

**Endpoint:** `GET /conversation/{conversation_id}`

**Request:**
```bash
curl -X GET http://127.0.0.1:8000/conversation/663434ef-1314-4857-ae3a-e05ac8e1bdce
```

**Response:**
```json
{
  "conversation_id": "663434ef-1314-4857-ae3a-e05ac8e1bdce",
  "messages": [
    {
      "role": "scammer",
      "content": "Your account has been flagged"
    },
    {
      "role": "honeypot",
      "content": "I can provide my details"
    }
  ],
  "persona": "elderly_person",
  "engagement_level": 20,
  "extracted_intelligence": {
    "bank_accounts": ["1234567890"],
    "upi_ids": [],
    "phishing_links": [],
    "phone_numbers": [],
    "email_addresses": [],
    "suspicious_patterns": []
  }
}
```

---

### 5. Terminate Conversation

**Endpoint:** `POST /terminate/{conversation_id}`

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/terminate/663434ef-1314-4857-ae3a-e05ac8e1bdce
```

**Response:**
```json
{
  "status": "success",
  "message": "Conversation 663434ef-1314-4857-ae3a-e05ac8e1bdce terminated",
  "conversation_id": "663434ef-1314-4857-ae3a-e05ac8e1bdce"
}
```

---

### 6. Get System Statistics

**Endpoint:** `GET /stats`

**Request:**
```bash
curl -X GET http://127.0.0.1:8000/stats
```

**Response:**
```json
{
  "active_conversations": 1,
  "total_messages": 4,
  "system_status": "operational"
}
```

---

## Scam Detection Algorithm

The system detects scams using:

1. **Keyword Matching** - Searches for known scam-related keywords
2. **URL Detection** - Identifies suspicious links
3. **Urgency Patterns** - Detects time-pressure tactics
4. **Information Requests** - Identifies requests for sensitive data

### Scam Types Detected

- **Banking**: Account verification, password requests
- **UPI**: Payment requests, UPI ID extraction
- **Phishing**: Malicious links, credential requests
- **Investment**: Guaranteed returns, quick money
- **Romance**: Love scams, financial emergencies

---

## Intelligence Extraction

Automatically extracts:

- **Bank Accounts**: 10-18 digit numbers
- **UPI IDs**: username@bank format
- **Phishing Links**: HTTP/HTTPS URLs
- **Phone Numbers**: Various international formats
- **Email Addresses**: Standard email format
- **Suspicious Patterns**: Regex matches for scam indicators

---

## Engagement Personas

The system uses different personas to engage realistically:

1. **Elderly Person** (default)
   - Tech-naive but willing to help
   - Asks clarifying questions
   - Polite and trusting

2. **Curious User**
   - Interested in making quick money
   - Slightly cautious but willing to proceed
   - Brief and conversational

3. **Desperate Person**
   - In financial difficulty
   - Less questioning
   - Eager and compliant

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK` - Successful request
- `404 Not Found` - Conversation not found
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Request/Response Models

### ScamMessage (Input)
```json
{
  "message": "string",           // Required: The scam message to analyze
  "sender_id": "string",         // Optional: Sender identifier
  "timestamp": "string"          // Optional: ISO format timestamp
}
```

### HoneypotResponse (Output)
```json
{
  "conversation_id": "string",
  "detected_scam": {
    "is_scam": "boolean",
    "confidence": "number (0-1)",
    "scam_type": "string or null",
    "reason": "string"
  },
  "ai_response": "string",
  "extracted_intelligence": {
    "bank_accounts": ["string"],
    "upi_ids": ["string"],
    "phishing_links": ["string"],
    "phone_numbers": ["string"],
    "email_addresses": ["string"],
    "suspicious_patterns": ["string"]
  },
  "conversation_state": {
    "conversation_id": "string",
    "engagement_level": "number (0-100)",
    "message_count": "number",
    "is_active": "boolean"
  }
}
```

---

## Testing with cURL

See `test_api.py` for Python example or use these cURL commands directly.

### Quick Test
```bash
# Health check
curl http://127.0.0.1:8000/health

# Analyze message
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"message":"Send money to my bank account"}'
```

---

## Rate Limiting & Production Notes

- Current implementation has no rate limiting (add for production)
- Conversations stored in memory (add database for persistence)
- Add authentication for production deployment
- Consider adding request logging for audit trail
- Implement conversation timeout for abandoned sessions

---

## Integration with Mock Scammer API

To integrate with a real Mock Scammer API:

1. Update `.env` with your API endpoint:
   ```
   MOCK_SCAMMER_API_URL=http://your-mock-api.com
   MOCK_SCAMMER_API_KEY=your-api-key
   ```

2. The `MockScammerAPI` class in `app/services/mock_scammer_api.py` is ready to use

3. Call it from engagement routes as needed

---

## Support

For issues or questions, refer to the main README.md or review the source code in `app/` directory.
