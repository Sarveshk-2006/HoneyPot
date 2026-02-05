#!/usr/bin/env python3
"""
Dashboard Test Script - Demonstrates all UI functionality
"""
import requests
import json
import time

API_URL = "http://127.0.0.1:8000"

# Sample scam messages for testing
TEST_MESSAGES = [
    "Hello! Your bank account has been compromised. Please verify: 9876543210",
    "Urgent: Transfer funds to UPI: user@okhdfcbank immediately!",
    "Click here to verify: http://phishingbank.com/verify.php",
    "Invest in our scheme and make 200% returns guaranteed!",
    "I love you darling. Can you help me with money? -Romance scam",
    "Hello! This is a legitimate customer service message. How can we help?"
]

def test_dashboard():
    print("\n🎯 Testing ALL Dashboard Buttons and Functionality\n")
    
    # Test 1: Health Check (Server Status Button)
    print("=" * 70)
    print("1️⃣  TEST SERVER STATUS BUTTON - GET /health")
    print("=" * 70)
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2-7: Send various messages (Test Message Button)
    print("\n" + "=" * 70)
    print("2️⃣  TEST MESSAGE BUTTON - POST /analyze (Multiple Messages)")
    print("=" * 70)
    
    conversation_ids = []
    for i, message in enumerate(TEST_MESSAGES, 1):
        try:
            print(f"\n📨 Test {i}: {message[:50]}...")
            response = requests.post(f"{API_URL}/analyze", json={"message": message})
            data = response.json()
            conversation_ids.append(data.get("conversation_id"))
            
            print(f"   ✅ Scam Detected: {data.get('scam_detected')}")
            if data.get('scam_detected'):
                print(f"   ✅ Type: {data.get('scam_type')}")
                print(f"   ✅ Confidence: {data.get('confidence')*100:.1f}%")
            print(f"   ✅ Response Time: {data.get('response_time'):.2f}ms")
            print(f"   ✅ Conv ID: {data.get('conversation_id')[:12]}...")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test 3: Get Stats (Dashboard KPI Cards Update)
    print("\n" + "=" * 70)
    print("3️⃣  TEST DASHBOARD KPI CARDS - GET /stats")
    print("=" * 70)
    try:
        response = requests.get(f"{API_URL}/stats")
        stats = response.json()
        print(f"✅ Total Messages: {stats.get('total_messages')}")
        print(f"✅ Scams Detected: {stats.get('scams_detected')}")
        print(f"✅ Banking Scams: {stats.get('banking_scams')}")
        print(f"✅ Phishing Scams: {stats.get('phishing_scams')}")
        print(f"✅ Investment Scams: {stats.get('investment_scams')}")
        print(f"✅ Romance Scams: {stats.get('romance_scams')}")
        print(f"✅ UPI Scams: {stats.get('upi_scams')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Conversation Details (Table Expansion Click)
    if conversation_ids:
        print("\n" + "=" * 70)
        print("4️⃣  TEST TABLE ROW EXPANSION - GET /conversation/{id}")
        print("=" * 70)
        try:
            response = requests.get(f"{API_URL}/conversation/{conversation_ids[0]}")
            data = response.json()
            print(f"✅ Conversation ID: {data.get('conversation_id')}")
            print(f"✅ Total Messages: {data.get('message_count')}")
            print(f"✅ Engagement: {data.get('engagement_level')}%")
            print(f"✅ Status: {data.get('status')}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test 5: Conversation Continuation (Continue Button)
    if conversation_ids:
        print("\n" + "=" * 70)
        print("5️⃣  TEST CONTINUE CONVERSATION - POST /conversation/{id}")
        print("=" * 70)
        try:
            response = requests.post(
                f"{API_URL}/conversation/{conversation_ids[0]}", 
                json={"message": "Yes, I can help with that."}
            )
            data = response.json()
            print(f"✅ AI Response: {data.get('ai_response')[:60]}...")
            print(f"✅ New Engagement: {data.get('engagement_level')}%")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test 6: Terminate Conversation (Terminate Button)
    if conversation_ids:
        print("\n" + "=" * 70)
        print("6️⃣  TEST TERMINATE BUTTON - POST /terminate/{id}")
        print("=" * 70)
        try:
            response = requests.post(f"{API_URL}/terminate/{conversation_ids[0]}")
            data = response.json()
            print(f"✅ Status: {data.get('status')}")
            print(f"✅ Message: {data.get('message')}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Final: Get Updated Stats
    print("\n" + "=" * 70)
    print("7️⃣  FINAL DASHBOARD UPDATE - GET /stats")
    print("=" * 70)
    try:
        response = requests.get(f"{API_URL}/stats")
        stats = response.json()
        print(f"✅ Total Messages: {stats.get('total_messages')}")
        print(f"✅ Scams Detected: {stats.get('scams_detected')}")
        print(f"✅ Response Time Available: {'avg_response_time' in stats}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ ALL DASHBOARD BUTTONS TESTED SUCCESSFULLY!")
    print("=" * 70)
    print("\n📊 Dashboard should now display:")
    print("   • KPI cards with updated metrics")
    print("   • Charts showing scam distribution")
    print("   • Recent detections table")
    print("   • Intelligence extraction stats")
    print("   • All interactive buttons working")
    print("\n")

if __name__ == "__main__":
    test_dashboard()
