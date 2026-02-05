import requests
import json
import time
import statistics
from typing import List, Dict, Tuple

BASE_URL = "http://127.0.0.1:8000"

class HoneypotTester:
    """Comprehensive test suite for Agentic Honeypot"""
    
    def __init__(self):
        self.results = []
        self.timings = []
        self.conversations = []
        
    def test_health(self) -> bool:
        """Test health check endpoint"""
        print("\n" + "="*70)
        print("TEST 1: Health Check")
        print("="*70)
        
        try:
            start = time.time()
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            elapsed = (time.time() - start) * 1000
            
            self.timings.append(elapsed)
            
            print(f"✅ Status Code: {response.status_code}")
            data = response.json()
            print(f"✅ Service: {data.get('service')}")
            print(f"✅ Status: {data.get('status')}")
            print(f"✅ Active Conversations: {data.get('active_conversations')}")
            print(f"⏱️  Response Time: {elapsed:.2f}ms")
            
            self.results.append(("Health Check", True, elapsed))
            return True
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.results.append(("Health Check", False, 0))
            return False
    
    def test_banking_scam(self) -> Tuple[bool, str]:
        """Test banking scam detection and engagement"""
        print("\n" + "="*70)
        print("TEST 2: Banking Scam Detection & Engagement")
        print("="*70)
        
        payload = {
            "message": "Hello! Your bank account has been compromised due to suspicious activity. Please click here immediately to verify your identity: http://secure-bank-verify.com. Enter your password and OTP to confirm.",
            "sender_id": "scammer_bank_001"
        }
        
        try:
            start = time.time()
            response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=5)
            elapsed = (time.time() - start) * 1000
            
            self.timings.append(elapsed)
            
            if response.status_code != 200:
                print(f"❌ Status Code: {response.status_code}")
                self.results.append(("Banking Scam Detection", False, elapsed))
                return False, None
            
            data = response.json()
            conversation_id = data['conversation_id']
            
            print(f"✅ Conversation ID: {conversation_id}")
            print(f"✅ Scam Detected: {data['detected_scam']['is_scam']}")
            print(f"✅ Scam Type: {data['detected_scam']['scam_type']}")
            print(f"✅ Confidence: {data['detected_scam']['confidence']:.2%}")
            print(f"✅ AI Response: {data['ai_response']}")
            
            # Check extracted intelligence
            intel = data['extracted_intelligence']
            if intel['phishing_links']:
                print(f"✅ Phishing Links Found: {intel['phishing_links']}")
            
            print(f"⏱️  Response Time: {elapsed:.2f}ms")
            
            self.conversations.append(conversation_id)
            self.results.append(("Banking Scam Detection", True, elapsed))
            return True, conversation_id
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.results.append(("Banking Scam Detection", False, 0))
            return False, None
    
    def test_continuation(self, conversation_id: str) -> bool:
        """Test conversation continuation"""
        print("\n" + "="*70)
        print("TEST 3: Conversation Continuation")
        print("="*70)
        
        payload = {
            "message": "Yes, I understand. I have my bank account number ready: 9876543210. What should I do next? Should I provide my password as well?"
        }
        
        try:
            start = time.time()
            response = requests.post(
                f"{BASE_URL}/conversation/{conversation_id}",
                json=payload,
                timeout=5
            )
            elapsed = (time.time() - start) * 1000
            
            self.timings.append(elapsed)
            
            if response.status_code != 200:
                print(f"❌ Status Code: {response.status_code}")
                self.results.append(("Conversation Continuation", False, elapsed))
                return False
            
            data = response.json()
            
            print(f"✅ Conversation ID: {conversation_id}")
            print(f"✅ New AI Response: {data['ai_response']}")
            print(f"✅ Engagement Level: {data['conversation_state']['engagement_level']}%")
            print(f"✅ Message Count: {data['conversation_state']['message_count']}")
            
            # Check for bank account extraction
            intel = data['extracted_intelligence']
            if intel['bank_accounts']:
                print(f"✅ Bank Accounts Extracted: {intel['bank_accounts']}")
            
            print(f"⏱️  Response Time: {elapsed:.2f}ms")
            
            self.results.append(("Conversation Continuation", True, elapsed))
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.results.append(("Conversation Continuation", False, 0))
            return False
    
    def test_upi_scam(self) -> Tuple[bool, str]:
        """Test UPI scam detection"""
        print("\n" + "="*70)
        print("TEST 4: UPI Scam Detection")
        print("="*70)
        
        payload = {
            "message": "Congratulations! You have won a prize of Rs. 100,000! Please send Rs. 500 immediately to user@okhdfcbank to claim your reward. Limited time offer!",
            "sender_id": "scammer_upi_001"
        }
        
        try:
            start = time.time()
            response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=5)
            elapsed = (time.time() - start) * 1000
            
            self.timings.append(elapsed)
            
            if response.status_code != 200:
                self.results.append(("UPI Scam Detection", False, elapsed))
                return False, None
            
            data = response.json()
            conversation_id = data['conversation_id']
            
            print(f"✅ Conversation ID: {conversation_id}")
            print(f"✅ Scam Detected: {data['detected_scam']['is_scam']}")
            print(f"✅ Confidence: {data['detected_scam']['confidence']:.2%}")
            
            intel = data['extracted_intelligence']
            if intel['upi_ids']:
                print(f"✅ UPI IDs Found: {intel['upi_ids']}")
            
            print(f"⏱️  Response Time: {elapsed:.2f}ms")
            
            self.conversations.append(conversation_id)
            self.results.append(("UPI Scam Detection", True, elapsed))
            return True, conversation_id
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.results.append(("UPI Scam Detection", False, 0))
            return False, None
    
    def test_get_conversation(self, conversation_id: str) -> bool:
        """Test retrieving conversation details"""
        print("\n" + "="*70)
        print("TEST 5: Get Conversation Details")
        print("="*70)
        
        try:
            start = time.time()
            response = requests.get(
                f"{BASE_URL}/conversation/{conversation_id}",
                timeout=5
            )
            elapsed = (time.time() - start) * 1000
            
            self.timings.append(elapsed)
            
            if response.status_code != 200:
                self.results.append(("Get Conversation", False, elapsed))
                return False
            
            data = response.json()
            
            print(f"✅ Conversation ID: {data['conversation_id']}")
            print(f"✅ Persona: {data['persona']}")
            print(f"✅ Messages: {len(data['messages'])}")
            print(f"✅ Engagement Level: {data['engagement_level']}%")
            
            print(f"\n📝 Message History:")
            for i, msg in enumerate(data['messages'][:4], 1):  # Show first 4 messages
                role = "👤 Scammer" if msg['role'] == 'scammer' else "🤖 Honeypot"
                print(f"   {i}. {role}: {msg['content'][:60]}...")
            
            print(f"\n⏱️  Response Time: {elapsed:.2f}ms")
            
            self.results.append(("Get Conversation", True, elapsed))
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.results.append(("Get Conversation", False, 0))
            return False
    
    def test_stats(self) -> bool:
        """Test statistics endpoint"""
        print("\n" + "="*70)
        print("TEST 6: System Statistics")
        print("="*70)
        
        try:
            start = time.time()
            response = requests.get(f"{BASE_URL}/stats", timeout=5)
            elapsed = (time.time() - start) * 1000
            
            self.timings.append(elapsed)
            
            if response.status_code != 200:
                self.results.append(("System Statistics", False, elapsed))
                return False
            
            data = response.json()
            
            print(f"✅ Active Conversations: {data['active_conversations']}")
            print(f"✅ Total Messages: {data['total_messages']}")
            print(f"✅ System Status: {data['system_status']}")
            print(f"⏱️  Response Time: {elapsed:.2f}ms")
            
            self.results.append(("System Statistics", True, elapsed))
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.results.append(("System Statistics", False, 0))
            return False
    
    def test_terminate(self, conversation_id: str) -> bool:
        """Test conversation termination"""
        print("\n" + "="*70)
        print("TEST 7: Terminate Conversation")
        print("="*70)
        
        try:
            start = time.time()
            response = requests.post(
                f"{BASE_URL}/terminate/{conversation_id}",
                timeout=5
            )
            elapsed = (time.time() - start) * 1000
            
            self.timings.append(elapsed)
            
            if response.status_code != 200:
                self.results.append(("Terminate Conversation", False, elapsed))
                return False
            
            data = response.json()
            
            print(f"✅ Status: {data['status']}")
            print(f"✅ Message: {data['message']}")
            print(f"⏱️  Response Time: {elapsed:.2f}ms")
            
            self.results.append(("Terminate Conversation", True, elapsed))
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.results.append(("Terminate Conversation", False, 0))
            return False
    
    def test_legitimate_message(self) -> bool:
        """Test legitimate message handling"""
        print("\n" + "="*70)
        print("TEST 8: Legitimate Message Detection")
        print("="*70)
        
        payload = {
            "message": "Hi, how are you doing today? I hope you're having a great day!",
            "sender_id": "normal_user"
        }
        
        try:
            start = time.time()
            response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=5)
            elapsed = (time.time() - start) * 1000
            
            self.timings.append(elapsed)
            
            if response.status_code != 200:
                self.results.append(("Legitimate Message", False, elapsed))
                return False
            
            data = response.json()
            
            is_legitimate = not data['detected_scam']['is_scam']
            print(f"✅ Scam Detected: {data['detected_scam']['is_scam']}")
            print(f"✅ Correctly Identified as Legitimate: {is_legitimate}")
            print(f"✅ AI Response: {data['ai_response']}")
            print(f"⏱️  Response Time: {elapsed:.2f}ms")
            
            self.results.append(("Legitimate Message", is_legitimate, elapsed))
            return is_legitimate
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.results.append(("Legitimate Message", False, 0))
            return False
    
    def display_summary(self):
        """Display test summary"""
        print("\n\n" + "="*70)
        print("📊 TEST EXECUTION SUMMARY")
        print("="*70)
        
        passed = sum(1 for _, result, _ in self.results if result)
        total = len(self.results)
        
        print(f"\n✅ Tests Passed: {passed}/{total}")
        
        print("\n📋 Test Results:")
        print("-" * 70)
        for test_name, result, timing in self.results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status:10} | {test_name:30} | {timing:7.2f}ms")
        
        if self.timings:
            print("-" * 70)
            print(f"\n⏱️  Performance Metrics:")
            print(f"   Average Response Time: {statistics.mean(self.timings):.2f}ms")
            print(f"   Min Response Time:     {min(self.timings):.2f}ms")
            print(f"   Max Response Time:     {max(self.timings):.2f}ms")
            print(f"   Std Deviation:         {statistics.stdev(self.timings) if len(self.timings) > 1 else 0:.2f}ms")
        
        print("\n" + "="*70)
        if passed == total:
            print("🏆 ALL TESTS PASSED! System is fully operational.")
        else:
            print(f"⚠️  {total - passed} test(s) failed. Please review the output above.")
        print("="*70 + "\n")


def main():
    """Run comprehensive test suite"""
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " "*10 + "🚨 AGENTIC HONEYPOT - COMPREHENSIVE TEST SUITE 🚨" + " "*10 + "║")
    print("╚" + "═"*68 + "╝")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("\n✅ Server is running!")
        else:
            print("\n⚠️  Server might not be responding correctly")
    except:
        print("\n❌ ERROR: Server is not running!")
        print("   Start the server with: python -m uvicorn app.main:app --reload")
        return
    
    # Run tests
    tester = HoneypotTester()
    
    # Execute all tests
    tester.test_health()
    success, conv_id_1 = tester.test_banking_scam()
    if success:
        tester.test_continuation(conv_id_1)
        tester.test_get_conversation(conv_id_1)
        tester.test_terminate(conv_id_1)
    
    success, conv_id_2 = tester.test_upi_scam()
    tester.test_legitimate_message()
    tester.test_stats()
    
    # Display summary
    tester.display_summary()


if __name__ == "__main__":
    main()
