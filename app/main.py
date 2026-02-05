from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uuid
import time
from pathlib import Path
from app.models import ScamMessage, HoneypotResponse, ExtractedIntelligence
from app.services.detector import ScamDetector
from app.services.extractor import IntelligenceExtractor
from app.agents.engagement_agent import EngagementAgent
from app.config import Config
from app.logger import logger, APILogger

# Initialize FastAPI app with enhanced configuration
app = FastAPI(
    title="Agentic Honeypot for Scam Detection",
    description="Autonomous AI honeypot system that detects scams and extracts intelligence",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (Dashboard UI)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    logger.info("📊 Web Dashboard mounted at /static")
else:
    logger.warning("⚠️ Static files directory not found")

# Initialize services
detector = ScamDetector()
extractor = IntelligenceExtractor()
agent = EngagementAgent()

logger.info("🚀 Agentic Honeypot System Initialized")
logger.info(f"📍 Server: {Config.HOST}:{Config.PORT}")
logger.info(f"🔍 Debug Mode: {Config.DEBUG}")


@app.get("/")
async def dashboard():
    """Serve the web dashboard"""
    from fastapi.responses import FileResponse
    dashboard_path = Path(__file__).parent / "static" / "index.html"
    if dashboard_path.exists():
        return FileResponse(dashboard_path)
    return {"message": "Dashboard not found. Visit /docs for API documentation."}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check requested")
    return {
        "status": "healthy",
        "service": "Agentic Honeypot",
        "version": "1.0.0",
        "active_conversations": len(agent.conversation_states)
    }


@app.post("/analyze")
async def analyze_scam(message: ScamMessage) -> HoneypotResponse:
    """
    Main endpoint to analyze a message and engage with scammer
    
    Args:
        message: ScamMessage containing the incoming message
        
    Returns:
        HoneypotResponse with detection results and engagement
    """
    conversation_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        APILogger.log_request("/analyze", "POST", {"message_length": len(message.message)})
        
        # Detect scam
        detection = detector.detect_scam(message.message)
        
        if detection.is_scam:
            APILogger.log_scam_detected(conversation_id, detection.scam_type.value if detection.scam_type else "unknown", detection.confidence)
        
        # Extract intelligence
        intelligence = extractor.extract_intelligence(message.message)
        
        # Log extracted data
        total_intel = (len(intelligence.bank_accounts) + len(intelligence.upi_ids) + 
                       len(intelligence.phishing_links) + len(intelligence.phone_numbers) + 
                       len(intelligence.email_addresses))
        if total_intel > 0:
            APILogger.log_intelligence_extracted(conversation_id, "data points", total_intel)
        
        # Generate engagement response
        ai_response = ""
        if detection.is_scam:
            try:
                ai_response = await agent.engage_with_scammer(
                    conversation_id=conversation_id,
                    scammer_message=message.message,
                    scam_type=detection.scam_type,
                    persona="elderly_person"
                )
            except Exception as e:
                logger.warning(f"Engagement error: {str(e)}")
                ai_response = f"Error engaging with scammer: {str(e)}"
        else:
            ai_response = "Message does not appear to be a scam. No engagement needed."
        
        # Get conversation state for response
        conv_state = agent.get_conversation_state(conversation_id)
        state_dict = {
            "conversation_id": conversation_id,
            "engagement_level": conv_state.engagement_level if conv_state else 0,
            "message_count": len(conv_state.messages) if conv_state else 0,
            "is_active": True
        }
        
        response = HoneypotResponse(
            conversation_id=conversation_id,
            detected_scam=detection,
            ai_response=ai_response,
            extracted_intelligence=intelligence,
            conversation_state=state_dict
        )
        
        elapsed_time = (time.time() - start_time) * 1000
        APILogger.log_response("/analyze", 200, elapsed_time)
        
        return response
        
    except Exception as e:
        logger.error(f"Error in /analyze: {str(e)}", exc_info=True)
        APILogger.log_error("/analyze", str(e), e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/conversation/{conversation_id}")
async def continue_conversation(conversation_id: str, message: ScamMessage) -> HoneypotResponse:
    """
    Continue an ongoing conversation with a scammer
    
    Args:
        conversation_id: ID of existing conversation
        message: Next message from scammer
        
    Returns:
        Updated conversation response
    """
    start_time = time.time()
    
    try:
        APILogger.log_request(f"/conversation/{conversation_id}", "POST", {"message_length": len(message.message)})
        
        # Detect scam in new message
        detection = detector.detect_scam(message.message)
        
        if detection.is_scam:
            APILogger.log_scam_detected(conversation_id, detection.scam_type.value if detection.scam_type else "unknown", detection.confidence)
        
        # Extract intelligence from entire conversation
        conv_state = agent.get_conversation_state(conversation_id)
        if conv_state:
            history = [msg["content"] for msg in conv_state.messages]
            intelligence = extractor.extract_intelligence(message.message, history)
        else:
            intelligence = extractor.extract_intelligence(message.message)
        
        # Log extracted data
        total_intel = (len(intelligence.bank_accounts) + len(intelligence.upi_ids) + 
                       len(intelligence.phishing_links) + len(intelligence.phone_numbers) + 
                       len(intelligence.email_addresses))
        if total_intel > 0:
            APILogger.log_intelligence_extracted(conversation_id, "data points", total_intel)
        
        # Generate engagement response
        ai_response = await agent.engage_with_scammer(
            conversation_id=conversation_id,
            scammer_message=message.message,
            scam_type=detection.scam_type
        )
        
        # Get updated conversation state
        conv_state = agent.get_conversation_state(conversation_id)
        state_dict = {
            "conversation_id": conversation_id,
            "engagement_level": conv_state.engagement_level if conv_state else 0,
            "message_count": len(conv_state.messages) if conv_state else 0,
            "is_active": True
        }
        
        if conv_state:
            APILogger.log_engagement(conversation_id, conv_state.engagement_level)
        
        response = HoneypotResponse(
            conversation_id=conversation_id,
            detected_scam=detection,
            ai_response=ai_response,
            extracted_intelligence=intelligence,
            conversation_state=state_dict
        )
        
        elapsed_time = (time.time() - start_time) * 1000
        APILogger.log_response(f"/conversation/{conversation_id}", 200, elapsed_time)
        
        return response
        
    except Exception as e:
        logger.error(f"Error in /conversation: {str(e)}", exc_info=True)
        APILogger.log_error(f"/conversation/{conversation_id}", str(e), e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get details of a specific conversation"""
    start_time = time.time()
    APILogger.log_request(f"/conversation/{conversation_id}", "GET")
    
    conv_state = agent.get_conversation_state(conversation_id)
    
    if not conv_state:
        logger.warning(f"Conversation not found: {conversation_id}")
        APILogger.log_error(f"/conversation/{conversation_id}", "Not found")
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    response = {
        "conversation_id": conversation_id,
        "messages": conv_state.messages,
        "persona": conv_state.scammer_persona,
        "engagement_level": conv_state.engagement_level,
        "extracted_intelligence": conv_state.extracted_intel.model_dump()
    }
    
    elapsed_time = (time.time() - start_time) * 1000
    APILogger.log_response(f"/conversation/{conversation_id}", 200, elapsed_time)
    
    return response


@app.post("/terminate/{conversation_id}")
async def terminate_conversation(conversation_id: str):
    """Terminate a conversation"""
    start_time = time.time()
    APILogger.log_request(f"/terminate/{conversation_id}", "POST")
    
    if agent.terminate_conversation(conversation_id):
        logger.info(f"Conversation terminated: {conversation_id}")
        response = {
            "status": "success",
            "message": f"Conversation {conversation_id} terminated",
            "conversation_id": conversation_id
        }
        
        elapsed_time = (time.time() - start_time) * 1000
        APILogger.log_response(f"/terminate/{conversation_id}", 200, elapsed_time)
        
        return response
    else:
        logger.warning(f"Conversation not found for termination: {conversation_id}")
        APILogger.log_error(f"/terminate/{conversation_id}", "Not found")
        raise HTTPException(status_code=404, detail="Conversation not found")


@app.get("/stats")
async def get_stats():
    """Get honeypot statistics"""
    start_time = time.time()
    APILogger.log_request("/stats", "GET")
    
    active_conversations = len(agent.conversation_states)
    total_messages = sum(len(state.messages) for state in agent.conversation_states.values())
    
    stats = {
        "active_conversations": active_conversations,
        "total_messages": total_messages,
        "system_status": "operational",
        "timestamp": time.time()
    }
    
    elapsed_time = (time.time() - start_time) * 1000
    APILogger.log_response("/stats", 200, elapsed_time)
    logger.info(f"📊 Stats: {active_conversations} active conversations, {total_messages} messages")
    
    return stats


# This allows running with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    logger.info(f"🌐 Starting server on {Config.HOST}:{Config.PORT}")
    uvicorn.run(app, host=Config.HOST, port=Config.PORT, reload=Config.DEBUG)
