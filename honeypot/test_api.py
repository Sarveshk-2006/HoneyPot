import requests
import json
import time

# Wait a moment for server to start
time.sleep(2)

BASE_URL = "http://127.0.0.1:8000"

print("=" * 70)
print("AGENTIC HONEYPOT - API DEMONSTRATION")
print("=" * 70)

# Test 1: Health check
print("\n1. Health Check:")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Analyze Banking Scam
print("\n2. Analyze Banking Scam Message:")
print("-" * 70)
banking_scam = {
    "message": "Hello! Your bank account has been flagged for suspicious activity. Please verify your account immediately by clicking here: http://verify-bank-account.com. Enter your password and OTP to confirm.",
    "sender_id": "scammer_001",
    "timestamp": "2024-02-05T10:30:00"
}
try:
    response = requests.post(f"{BASE_URL}/analyze", json=banking_scam)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Conversation ID: {data['conversation_id']}")
    print(f"Detected Scam: {json.dumps(data['detected_scam'], indent=2)}")
    print(f"AI Response: {data['ai_response']}")
    print(f"Extracted Intelligence:")
    intel = data['extracted_intelligence']
    if intel['phishing_links']:
        print(f"  - Phishing Links: {intel['phishing_links']}")
    if intel['suspicious_patterns']:
        print(f"  - Suspicious Patterns: {intel['suspicious_patterns'][:3]}")
    
    conversation_id_1 = data['conversation_id']
except Exception as e:
    print(f"Error: {e}")

# Test 3: Analyze UPI Scam
print("\n3. Analyze UPI Scam Message:")
print("-" * 70)
upi_scam = {
    "message": "Hello! You have won a prize! Send money to user@okhdfcbank to claim your reward of Rs. 50,000. Limited time offer!",
}
try:
    response = requests.post(f"{BASE_URL}/analyze", json=upi_scam)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Conversation ID: {data['conversation_id']}")
    print(f"Detected Scam: {json.dumps(data['detected_scam'], indent=2)}")
    print(f"AI Response: {data['ai_response']}")
    intel = data['extracted_intelligence']
    if intel['upi_ids']:
        print(f"Extracted UPI IDs: {intel['upi_ids']}")
    
    conversation_id_2 = data['conversation_id']
except Exception as e:
    print(f"Error: {e}")

# Test 4: Continue Conversation
print("\n4. Continue Banking Scam Conversation:")
print("-" * 70)
follow_up = {
    "message": "Here is my bank account number: 1234567890. Please let me know what to do next."
}
try:
    response = requests.post(f"{BASE_URL}/conversation/{conversation_id_1}", json=follow_up)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Conversation State: {json.dumps(data['conversation_state'], indent=2)}")
    print(f"Updated AI Response: {data['ai_response']}")
    intel = data['extracted_intelligence']
    if intel['bank_accounts']:
        print(f"Extracted Bank Accounts: {intel['bank_accounts']}")
except Exception as e:
    print(f"Error: {e}")

# Test 5: Get Conversation Details
print("\n5. Get Conversation Details:")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/conversation/{conversation_id_1}")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Persona: {data['persona']}")
    print(f"Engagement Level: {data['engagement_level']}")
    print(f"Message Count: {len(data['messages'])}")
    print(f"Extracted Intelligence Summary:")
    intel = data['extracted_intelligence']
    print(f"  - Bank Accounts: {intel['bank_accounts']}")
    print(f"  - UPI IDs: {intel['upi_ids']}")
    print(f"  - Phishing Links: {intel['phishing_links']}")
except Exception as e:
    print(f"Error: {e}")

# Test 6: Get Statistics
print("\n6. Get System Statistics:")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status: {response.status_code}")
    print(f"Stats: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test 7: Legitimate Message
print("\n7. Analyze Legitimate Message:")
print("-" * 70)
legit_msg = {
    "message": "Hi, how are you doing today?"
}
try:
    response = requests.post(f"{BASE_URL}/analyze", json=legit_msg)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Detected Scam: {json.dumps(data['detected_scam'], indent=2)}")
    print(f"AI Response: {data['ai_response']}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 70)
print("DEMONSTRATION COMPLETE")
print("=" * 70)
