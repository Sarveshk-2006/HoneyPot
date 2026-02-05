"""
Advanced Analytics Engine
Provides detailed analytics and insights about scam patterns
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict
import statistics

class AnalyticsEngine:
    """Advanced analytics for scam detection and intelligence"""
    
    def __init__(self):
        self.scam_history = []
        self.intelligence_history = []
        self.conversation_history = []
        self.hourly_stats = defaultdict(int)
        self.scam_type_counts = defaultdict(int)
        self.intelligence_type_counts = defaultdict(int)
    
    def record_scam_detection(self, scam_data: Dict[str, Any]):
        """Record a scam detection event"""
        detection_record = {
            'timestamp': datetime.now().isoformat(),
            'conversation_id': scam_data.get('conversation_id'),
            'scam_type': scam_data.get('scam_type'),
            'confidence': scam_data.get('confidence', 0),
            'message': scam_data.get('message', ''),
            'extracted_intel': scam_data.get('extracted_intel', [])
        }
        
        self.scam_history.append(detection_record)
        self.scam_type_counts[detection_record['scam_type']] += 1
        
        # Update hourly stats
        hour_key = datetime.now().strftime('%Y-%m-%d %H:00')
        self.hourly_stats[hour_key] += 1
    
    def record_intelligence(self, intel_data: Dict[str, Any]):
        """Record extracted intelligence"""
        intel_record = {
            'timestamp': datetime.now().isoformat(),
            'conversation_id': intel_data.get('conversation_id'),
            'intel_type': intel_data.get('type'),
            'value': intel_data.get('value'),
            'confidence': intel_data.get('confidence', 0)
        }
        
        self.intelligence_history.append(intel_record)
        self.intelligence_type_counts[intel_record['intel_type']] += 1
    
    def get_hourly_trend(self, hours: int = 24) -> Dict[str, int]:
        """Get hourly scam detection trend"""
        trend = {}
        for i in range(hours):
            time = (datetime.now() - timedelta(hours=i)).strftime('%Y-%m-%d %H:00')
            trend[time] = self.hourly_stats.get(time, 0)
        return dict(sorted(trend.items()))
    
    def get_high_risk_patterns(self) -> List[Dict[str, Any]]:
        """Identify high-risk scam patterns"""
        patterns = []
        
        for scam_type, count in self.scam_type_counts.items():
            # Get recent detections for this type
            recent = [s for s in self.scam_history if s['scam_type'] == scam_type][-10:]
            
            if recent:
                avg_confidence = statistics.mean([s['confidence'] for s in recent])
                pattern = {
                    'type': scam_type,
                    'occurrences': count,
                    'average_confidence': avg_confidence,
                    'risk_level': 'HIGH' if avg_confidence > 0.7 else 'MEDIUM' if avg_confidence > 0.4 else 'LOW',
                    'recent_count': len(recent)
                }
                patterns.append(pattern)
        
        return sorted(patterns, key=lambda x: x['average_confidence'], reverse=True)
    
    def get_most_targeted_intel_types(self) -> Dict[str, int]:
        """Get most targeted types of intelligence"""
        return dict(sorted(self.intelligence_type_counts.items(), key=lambda x: x[1], reverse=True))
    
    def get_conversation_analytics(self) -> Dict[str, Any]:
        """Get comprehensive conversation analytics"""
        if not self.scam_history:
            return {
                'total_scams': 0,
                'average_confidence': 0,
                'total_conversations': 0,
                'intelligence_extracted': 0
            }
        
        return {
            'total_scams': len(self.scam_history),
            'average_confidence': statistics.mean([s['confidence'] for s in self.scam_history]),
            'total_conversations': len(set(s['conversation_id'] for s in self.scam_history)),
            'intelligence_extracted': len(self.intelligence_history),
            'scam_type_distribution': dict(self.scam_type_counts),
            'intelligence_type_distribution': dict(self.intelligence_type_counts)
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        if not self.scam_history:
            return {
                'detection_rate': 0,
                'avg_confidence': 0,
                'patterns_identified': 0
            }
        
        recent_scams = self.scam_history[-100:]
        
        return {
            'detection_rate': len(recent_scams) / max(1, len(self.scam_history[-1000:])) * 100,
            'avg_confidence': statistics.mean([s['confidence'] for s in recent_scams]),
            'high_confidence_detections': len([s for s in recent_scams if s['confidence'] > 0.8]),
            'patterns_identified': len(self.get_high_risk_patterns()),
            'system_uptime': 'N/A'  # Would need server start time
        }
    
    def generate_report(self) -> str:
        """Generate comprehensive analytics report"""
        analytics = self.get_conversation_analytics()
        metrics = self.get_performance_metrics()
        patterns = self.get_high_risk_patterns()
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║         AGENTIC HONEYPOT - ANALYTICS REPORT             ║
╚══════════════════════════════════════════════════════════╝

📊 CONVERSATION ANALYTICS
├─ Total Scams Detected: {analytics['total_scams']}
├─ Average Confidence: {analytics['average_confidence']:.2%}
├─ Total Conversations: {analytics['total_conversations']}
└─ Intelligence Points Extracted: {analytics['intelligence_extracted']}

📈 SCAM TYPE DISTRIBUTION
"""
        for scam_type, count in sorted(analytics['scam_type_distribution'].items(), key=lambda x: x[1], reverse=True):
            report += f"├─ {scam_type.upper()}: {count}\n"
        
        report += f"""
🔍 INTELLIGENCE TYPE DISTRIBUTION
"""
        for intel_type, count in sorted(analytics['intelligence_type_distribution'].items(), key=lambda x: x[1], reverse=True):
            report += f"├─ {intel_type}: {count}\n"
        
        report += f"""
⚡ PERFORMANCE METRICS
├─ Detection Rate: {metrics['avg_confidence']:.2%}
├─ High Confidence Detections: {metrics['high_confidence_detections']}
├─ Patterns Identified: {metrics['patterns_identified']}
└─ System Status: Operational

🚨 HIGH-RISK PATTERNS
"""
        for pattern in patterns[:5]:
            report += f"├─ {pattern['type'].upper()}: {pattern['risk_level']} RISK ({pattern['average_confidence']:.2%} confidence)\n"
        
        report += "\n╚══════════════════════════════════════════════════════════╝\n"
        return report
    
    def export_analytics(self) -> Dict[str, Any]:
        """Export full analytics data"""
        return {
            'timestamp': datetime.now().isoformat(),
            'analytics': self.get_conversation_analytics(),
            'metrics': self.get_performance_metrics(),
            'patterns': self.get_high_risk_patterns(),
            'scam_history': self.scam_history[-50:],  # Last 50 detections
            'intelligence_history': self.intelligence_history[-50:]
        }

# Initialize global analytics engine
analytics_engine = AnalyticsEngine()
