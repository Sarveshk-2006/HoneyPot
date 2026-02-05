# Quick Start Guide - Agentic Honeypot

## 🚀 Start Server (Development)

```bash
cd d:\Buildathon\honeypot
venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Server available at: `http://127.0.0.1:8000`

---

## 📍 API Endpoints (Copy-Paste Ready)

### 1. Health Check
```bash
curl http://127.0.0.1:8000/health
```

### 2. Analyze Scam Message
```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Your bank account has been flagged. Verify here: http://fake-bank.com",
    "sender_id": "user123"
  }'
```

### 3. Continue Conversation
```bash
# Replace CONVERSATION_ID with the ID from response
curl -X POST http://127.0.0.1:8000/conversation/CONVERSATION_ID \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Here is my account number: 1234567890"
  }'
```

### 4. Get Conversation Details
```bash
curl http://127.0.0.1:8000/conversation/CONVERSATION_ID
```

### 5. Get System Stats
```bash
curl http://127.0.0.1:8000/stats
```

### 6. Terminate Conversation
```bash
curl -X POST http://127.0.0.1:8000/terminate/CONVERSATION_ID
```

---

## 📚 Interactive Documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 🧪 Run Tests

```bash
cd d:\Buildathon\honeypot
venv\Scripts\python -m pytest tests/test_honeypot.py -v
```

---

## 🎯 Testing the API (Python)

```bash
# Run the demo script
venv\Scripts\python test_api.py
```

---

## 📂 Project Structure

```
honeypot/
├── app/
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration
│   ├── models.py                  # Data models
│   ├── agents/
│   │   └── engagement_agent.py    # AI agent for scammer engagement
│   └── services/
│       ├── detector.py            # Scam detection
│       ├── extractor.py           # Intelligence extraction
│       └── mock_scammer_api.py    # Mock API client
├── tests/
│   └── test_honeypot.py          # Unit tests
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── README.md                       # Main documentation
├── API_DOCUMENTATION.md           # API reference
└── DEPLOYMENT.md                  # Deployment guide
```

---

## ⚙️ Configuration (.env)

```env
# OpenAI Integration
OPENAI_API_KEY=your_openai_key

# Mock Scammer API
MOCK_SCAMMER_API_URL=http://localhost:8001
MOCK_SCAMMER_API_KEY=your_api_key

# Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=true  # Set to 'false' for production
```

---

## 🔍 Scam Types Detected

1. **Banking** - Account verification, password requests
2. **UPI** - Payment requests, UPI IDs
3. **Phishing** - Malicious links, credential requests
4. **Investment** - Guaranteed returns, quick money
5. **Romance** - Love scams, financial emergencies

---

## 📊 Intelligence Extracted

- ✅ Bank account numbers
- ✅ UPI IDs
- ✅ Phishing links
- ✅ Phone numbers
- ✅ Email addresses
- ✅ Suspicious patterns

---

## 🎭 Engagement Personas

- **Elderly Person** (default) - Tech-naive, trusting
- **Curious User** - Interested, slightly cautious
- **Desperate Person** - Financial difficulty, eager

---

## 🆘 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process using it
taskkill /PID <PID> /F
```

### Dependency issues
```bash
# Reinstall dependencies
venv\Scripts\python -m pip install -r requirements.txt --force-reinstall
```

### Tests failing
```bash
# Run with verbose output
venv\Scripts\python -m pytest tests/ -v -s
```

---

## 📈 What's Working

✅ Scam detection with pattern matching
✅ Engagement personas for realistic interactions
✅ Intelligence extraction from conversations
✅ Conversation management and state tracking
✅ RESTful API with FastAPI
✅ Comprehensive test coverage (10/10 tests passing)
✅ JSON response format as required

---

## 🚀 Next Steps for Production

1. **Replace mock engagement** - Integrate real LLM API (OpenAI, Claude, etc.)
2. **Add database** - Store conversations persistently
3. **Implement authentication** - Secure API endpoints
4. **Deploy** - Use Docker/Kubernetes for scalability
5. **Monitor** - Set up logging and alerting
6. **Rate limiting** - Prevent abuse
7. **Mock Scammer API** - Connect to the provided mock API

---

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application with all endpoints |
| `models.py` | Pydantic models for request/response |
| `config.py` | Configuration settings |
| `detector.py` | Scam detection engine |
| `extractor.py` | Intelligence extraction logic |
| `engagement_agent.py` | AI agent for conversations |
| `mock_scammer_api.py` | Client for mock API |
| `test_honeypot.py` | Comprehensive unit tests |
| `test_api.py` | API demonstration script |

---

## 🎓 Key Features

1. **Autonomous Detection** - Automatically identifies scam attempts
2. **Active Engagement** - Responds with believable personas
3. **Intelligence Gathering** - Extracts sensitive information patterns
4. **Conversation Management** - Maintains context across messages
5. **Structured Output** - JSON format for easy integration
6. **Extensible** - Ready for LLM integration

---

## 📞 API Response Status Codes

- `200` - Success
- `404` - Conversation not found
- `500` - Server error

---

## 🔐 Production Checklist

- [ ] Set DEBUG=false in .env
- [ ] Add API authentication
- [ ] Enable HTTPS/SSL
- [ ] Set up database
- [ ] Configure rate limiting
- [ ] Enable logging
- [ ] Set up monitoring
- [ ] Deploy with gunicorn or similar
- [ ] Configure reverse proxy (nginx)
- [ ] Add health checks

---

**Ready to deploy?** See [DEPLOYMENT.md](DEPLOYMENT.md)
