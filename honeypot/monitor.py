"""
Real-time Honeypot Monitoring Dashboard
Displays live statistics about the honeypot system
"""

import requests
import json
import time
import os
from datetime import datetime
from typing import Dict

class HoneypotMonitor:
    """Monitor honeypot system in real-time"""
    
    def __init__(self, api_url: str = "http://127.0.0.1:8000"):
        self.api_url = api_url
        self.stats_history = []
        self.request_count = 0
        self.error_count = 0
        self.last_scam_detected = None
        
    def get_stats(self) -> Dict:
        """Get current statistics from API"""
        try:
            response = requests.get(f"{self.api_url}/stats", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"❌ Connection Error: {str(e)}")
            return None
    
    def health_check(self) -> bool:
        """Check if server is healthy"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def display_dashboard(self):
        """Display real-time monitoring dashboard"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 15 + "🚨 AGENTIC HONEYPOT - REAL-TIME MONITORING 🚨" + " " * 17 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        
        # Check server health
        if not self.health_check():
            print("❌ SERVER NOT RUNNING!")
            print("   Start the server with: python -m uvicorn app.main:app --reload")
            print()
            return False
        
        print("✅ Server Status: HEALTHY")
        print()
        
        # Get current stats
        stats = self.get_stats()
        if not stats:
            print("⚠️  Could not retrieve statistics")
            return False
        
        # Display statistics
        print("┌─ CURRENT METRICS " + "─" * 61 + "┐")
        print(f"│ 📊 Active Conversations: {stats.get('active_conversations', 0):<30}              │")
        print(f"│ 💬 Total Messages:       {stats.get('total_messages', 0):<30}              │")
        print(f"│ ⏰ Last Update:          {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<30}       │")
        print("└" + "─" * 77 + "┘")
        print()
        
        # Display trend
        if self.stats_history:
            prev_conversations = self.stats_history[-1].get('active_conversations', 0)
            curr_conversations = stats.get('active_conversations', 0)
            
            if curr_conversations > prev_conversations:
                print(f"📈 Conversations Trend: ↑ +{curr_conversations - prev_conversations}")
            elif curr_conversations < prev_conversations:
                print(f"📉 Conversations Trend: ↓ {curr_conversations - prev_conversations}")
            else:
                print(f"➡️  Conversations Trend: → Stable")
        
        print()
        
        # Display recent activity info
        print("┌─ API ENDPOINTS " + "─" * 62 + "┐")
        print(f"│ 🌐 Main API:      http://127.0.0.1:8000                         │")
        print(f"│ 📖 Swagger Docs:  http://127.0.0.1:8000/docs                    │")
        print(f"│ 📚 ReDoc:         http://127.0.0.1:8000/redoc                   │")
        print("└" + "─" * 77 + "┘")
        print()
        
        # Display quick commands
        print("┌─ QUICK COMMANDS " + "─" * 61 + "┐")
        print("│ 1️⃣  Test API:        python test_api.py                     │")
        print("│ 2️⃣  Run Tests:       pytest tests/test_honeypot.py -v       │")
        print("│ 3️⃣  View Logs:       tail -f logs/honeypot_*.log (Unix)     │")
        print("│ 4️⃣  Refresh Monitor: Run this script again                  │")
        print("└" + "─" * 77 + "┘")
        print()
        
        # Store history
        self.stats_history.append(stats)
        if len(self.stats_history) > 100:
            self.stats_history.pop(0)
        
        return True
    
    def continuous_monitor(self, interval: int = 5):
        """Run continuous monitoring with auto-refresh"""
        print("Starting continuous monitoring... (Press CTRL+C to stop)")
        print(f"Refresh interval: {interval} seconds")
        print()
        
        try:
            while True:
                self.display_dashboard()
                print(f"⏳ Next update in {interval} seconds... (CTRL+C to stop)")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n✅ Monitoring stopped.")
            print("📊 Final Statistics:")
            
            if self.stats_history:
                final_stats = self.stats_history[-1]
                print(f"   - Total conversations tracked: {final_stats.get('active_conversations', 0)}")
                print(f"   - Total messages processed: {final_stats.get('total_messages', 0)}")
                print(f"   - System uptime: {len(self.stats_history) * 5 // 60} minutes")


def main():
    """Main entry point for monitoring"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor Agentic Honeypot System')
    parser.add_argument('--url', default='http://127.0.0.1:8000', 
                        help='API URL (default: http://127.0.0.1:8000)')
    parser.add_argument('--interval', type=int, default=5,
                        help='Refresh interval in seconds (default: 5)')
    parser.add_argument('--once', action='store_true',
                        help='Show stats once and exit')
    
    args = parser.parse_args()
    
    monitor = HoneypotMonitor(api_url=args.url)
    
    if args.once:
        monitor.display_dashboard()
    else:
        monitor.continuous_monitor(interval=args.interval)


if __name__ == "__main__":
    main()
