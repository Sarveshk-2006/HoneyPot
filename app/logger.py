import logging
import sys
from datetime import datetime
import json
from pathlib import Path
import os

# Configure encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure logging
def setup_logger(name: str = "honeypot"):
    """Setup logging configuration"""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Create formatters without emojis for terminal
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console Handler (INFO level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File Handler (DEBUG level) - can include emojis
    file_handler = logging.FileHandler(f'logs/{name}_{datetime.now().strftime("%Y%m%d")}.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    return logger

# Create main logger
logger = setup_logger("honeypot")

class APILogger:
    """Log API requests and responses"""
    
    @staticmethod
    def log_request(endpoint: str, method: str, data: dict = None):
        """Log incoming request"""
        logger.info(f"[{method}] REQUEST: {endpoint}")
        if data:
            logger.debug(f"   Data: {json.dumps(data, indent=2)[:200]}...")
    
    @staticmethod
    def log_response(endpoint: str, status_code: int, response_time_ms: float):
        """Log outgoing response"""
        status_text = "OK" if status_code == 200 else f"ERROR{status_code}" if status_code >= 400 else "SUCCESS"
        logger.info(f"[{status_text}] RESPONSE: {endpoint} - {status_code} ({response_time_ms:.0f}ms)")
    
    @staticmethod
    def log_scam_detected(conversation_id: str, scam_type: str, confidence: float):
        """Log when scam is detected"""
        logger.warning(f"[ALERT] SCAM DETECTED: {scam_type} (confidence: {confidence:.2f}) - Conv: {conversation_id}")
    
    @staticmethod
    def log_intelligence_extracted(conversation_id: str, intel_type: str, count: int):
        """Log extracted intelligence"""
        logger.info(f"[DATA] EXTRACTED: {count} {intel_type} from conversation {conversation_id}")
    
    @staticmethod
    def log_engagement(conversation_id: str, engagement_level: int):
        """Log engagement progress"""
        logger.info(f"[ENGAGE] Level {engagement_level}% - Conv: {conversation_id}")
    
    @staticmethod
    def log_error(endpoint: str, error: str, exception=None):
        """Log errors"""
        logger.error(f"[ERROR] on {endpoint}: {error}")
        if exception:
            logger.debug(f"   Exception: {str(exception)}")

# Export logger
__all__ = ['logger', 'APILogger', 'setup_logger']

