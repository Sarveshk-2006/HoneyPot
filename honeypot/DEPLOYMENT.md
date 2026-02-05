# Deployment Guide - Agentic Honeypot

## Overview
This guide covers deploying the Agentic Honeypot system to various environments.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Services (AWS, Azure, Heroku)](#cloud-services)
4. [Production Configuration](#production-configuration)
5. [Monitoring & Logging](#monitoring--logging)

---

## Local Development

### Prerequisites
- Python 3.9+
- pip and virtualenv

### Steps

1. **Clone and setup**
```bash
cd honeypot
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Create .env file**
```bash
cp .env.example .env
# Edit with your configuration
```

3. **Run development server**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access APIs**
- Main API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ app/
COPY .env .env

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
# Build image
docker build -t honeypot:latest .

# Run container
docker run -p 8000:8000 \
    -e OPENAI_API_KEY=your_key \
    -e MOCK_SCAMMER_API_URL=http://api.example.com \
    honeypot:latest
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  honeypot:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - MOCK_SCAMMER_API_URL=${MOCK_SCAMMER_API_URL}
      - PORT=8000
      - HOST=0.0.0.0
      - DEBUG=false
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    
  # Optional: Reverse proxy (nginx)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - honeypot
```

Run with:
```bash
docker-compose up -d
```

---

## Cloud Services

### AWS Deployment (Elastic Beanstalk)

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize**
```bash
eb init -p python-3.11 honeypot
eb create honeypot-env
```

3. **Configure .ebextensions/python.config**
```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: /var/app/current:$PYTHONPATH
  aws:autoscaling:launchconfiguration:
    InstanceType: t3.micro
```

4. **Deploy**
```bash
eb deploy
```

### Azure App Service

1. **Create Resource Group**
```bash
az group create --name honeypot-rg --location eastus
```

2. **Create App Service Plan**
```bash
az appservice plan create \
    --name honeypot-plan \
    --resource-group honeypot-rg \
    --sku F1
```

3. **Create Web App**
```bash
az webapp create \
    --name honeypot-app \
    --resource-group honeypot-rg \
    --plan honeypot-plan \
    --runtime python:3.11
```

4. **Deploy from GitHub**
```bash
az webapp up --name honeypot-app --resource-group honeypot-rg
```

### Heroku Deployment

1. **Create Procfile**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. **Create Heroku app**
```bash
heroku create honeypot-app
```

3. **Set environment variables**
```bash
heroku config:set OPENAI_API_KEY=your_key
heroku config:set MOCK_SCAMMER_API_URL=http://api.example.com
```

4. **Deploy**
```bash
git push heroku main
```

---

## Production Configuration

### Environment Variables

**Essential:**
```
OPENAI_API_KEY=your_api_key
MOCK_SCAMMER_API_URL=https://api.example.com
PORT=8000
HOST=0.0.0.0
DEBUG=false
```

**Optional:**
```
LOG_LEVEL=INFO
MAX_CONVERSATION_LENGTH=50
SCAM_DETECTION_THRESHOLD=0.5
DATABASE_URL=postgresql://user:pass@localhost/honeypot
REDIS_URL=redis://localhost:6379
```

### Security Hardening

1. **Add HTTPS**
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with SSL
uvicorn app.main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem --host 0.0.0.0 --port 443
```

2. **Add API Authentication**

Create `app/auth.py`:
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthCredential

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthCredential = Depends(security)):
    if credentials.credentials != "your_secret_token":
        raise HTTPException(status_code=403, detail="Invalid token")
    return credentials.credentials
```

Update endpoints:
```python
@app.post("/analyze")
async def analyze_scam(
    message: ScamMessage,
    token: str = Depends(verify_token)
) -> HoneypotResponse:
    # ... endpoint code
```

3. **Add Rate Limiting**
```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/analyze")
@limiter.limit("10/minute")
async def analyze_scam(request: Request, message: ScamMessage):
    # ... endpoint code
```

4. **CORS Configuration**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### Database Integration

Update `app/config.py`:
```python
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./honeypot.db")
```

Use SQLAlchemy for persistent storage:
```bash
pip install sqlalchemy psycopg2
```

### Gunicorn Production Server

```bash
pip install gunicorn

# Run with 4 workers
gunicorn app.main:app -w 4 -b 0.0.0.0:8000 --access-logfile - --error-logfile -
```

---

## Monitoring & Logging

### Logging Setup

Create `app/logger.py`:
```python
import logging
import sys

logger = logging.getLogger("honeypot")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
```

### Application Metrics

Track with Prometheus:
```bash
pip install prometheus-client
```

```python
from prometheus_client import Counter, Histogram
from fastapi_prometheus_middleware import PrometheusMiddleware

scams_detected = Counter('scams_detected', 'Total scams detected')
response_time = Histogram('response_time', 'Response time in seconds')
```

### Health Checks

The `/health` endpoint is suitable for:
- Load balancer health checks
- Kubernetes liveness probes
- Uptime monitoring

Configure for your platform:

**Kubernetes:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 30
```

### Performance Optimization

1. **Enable Gzip Compression**
```python
from fastapi.middleware.gzip import GZIPMiddleware

app.add_middleware(GZIPMiddleware, minimum_size=1000)
```

2. **Database Connection Pooling**
```python
from sqlalchemy.pool import QueuePool

engine = create_engine(DATABASE_URL, poolclass=QueuePool)
```

3. **Caching**
```bash
pip install redis
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Memory Issues
```bash
# Monitor server memory
free -h

# Check Python memory
python -c "import psutil; print(psutil.Process().memory_info())"
```

### Connection Errors
- Check firewall rules
- Verify environment variables
- Test API endpoint connectivity
- Check logs for detailed errors

---

## Monitoring Dashboard

Recommended tools:
- **Prometheus** - Metrics collection
- **Grafana** - Visualization
- **ELK Stack** - Log aggregation
- **DataDog** - Full monitoring platform
- **NewRelic** - APM solution

---

## Continuous Deployment

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build & Deploy
        run: |
          docker build -t honeypot:latest .
          docker push your-registry/honeypot:latest
          # Deploy to your platform
```

---

## Support & Maintenance

- Monitor logs daily
- Update dependencies monthly
- Review security updates
- Test disaster recovery quarterly
- Maintain 99.5% uptime SLA

---

Last Updated: February 2024
