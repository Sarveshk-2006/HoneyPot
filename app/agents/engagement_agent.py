import json
import asyncio
from typing import List, Dict, Optional
from app.models import ConversationState, ScamType
from app.config import Config


class EngagementAgent:
    """AI agent that engages with scammers using believable personas"""
    
    # System prompts for different personas
    SYSTEM_PROMPTS = {
        'elderly_person': """You are a 65-year-old person who is somewhat tech-naive but willing to help. 
        You might be confused but eager to follow instructions. You ask clarifying questions but ultimately 
        comply with requests. You are polite and trusting. Keep responses short and natural.""",
        
        'curious_user': """You are a curious 30-year-old who found an interesting offer. 
        You're interested in making quick money but a bit cautious. You ask questions but are willing to proceed 
        if convinced. Keep responses brief and conversational.""",
        
        'desperate_person': """You are a person in financial difficulty who is desperate for money. 
        You're willing to take higher risks and are less questioning. You're eager and compliant. 
        Keep responses short but show desperation.""",
    }
    
    ENGAGEMENT_PROMPTS = {
        'banking': "Ask about what bank details they need and pretend to be looking for them.",
        'upi': "Express interest in the UPI transfer and ask for the UPI ID to send money.",
        'phishing': "Click on any links they provide and ask for more details on how to proceed.",
        'investment': "Show interest in the investment and ask for bank details to transfer money.",
        'romance': "Express emotional attachment and ask how they want you to send money.",
    }
    
    def __init__(self):
        self.conversation_states: Dict[str, ConversationState] = {}
    
    async def engage_with_scammer(
        self,
        conversation_id: str,
        scammer_message: str,
        scam_type: Optional[ScamType],
        persona: str = "elderly_person"
    ) -> str:
        """
        Generate an engagement response based on detected scam type
        
        Args:
            conversation_id: Unique conversation identifier
            scammer_message: Message from the scammer
            scam_type: Type of scam detected
            persona: Persona to use for engagement
            
        Returns:
            Response string to engage the scammer
        """
        
        # Initialize or retrieve conversation state
        if conversation_id not in self.conversation_states:
            self.conversation_states[conversation_id] = ConversationState(
                conversation_id=conversation_id,
                scammer_persona=persona
            )
        
        state = self.conversation_states[conversation_id]
        
        # Add scammer message to history
        state.messages.append({"role": "scammer", "content": scammer_message})
        
        # Build engagement prompt
        engagement_instruction = self._get_engagement_instruction(scam_type)
        system_prompt = self.SYSTEM_PROMPTS.get(persona, self.SYSTEM_PROMPTS['elderly_person'])
        
        # Generate response (simulated - in production use OpenAI API)
        response = await self._generate_response(
            system_prompt=system_prompt,
            user_message=scammer_message,
            engagement_instruction=engagement_instruction,
            conversation_history=state.messages
        )
        
        # Add our response to history
        state.messages.append({"role": "honeypot", "content": response})
        
        # Update engagement level
        state.engagement_level = min(state.engagement_level + 10, 100)
        
        return response
    
    def _get_engagement_instruction(self, scam_type: Optional[ScamType]) -> str:
        """Get specific engagement instruction for scam type"""
        if scam_type and scam_type.value in self.ENGAGEMENT_PROMPTS:
            return self.ENGAGEMENT_PROMPTS[scam_type.value]
        return "Continue engaging with the message and ask for more information."
    
    async def _generate_response(
        self,
        system_prompt: str,
        user_message: str,
        engagement_instruction: str,
        conversation_history: List[Dict[str, str]]
    ) -> str:
        """
        Generate AI response with improved context awareness
        
        In production, this would call OpenAI API or similar
        For now, returns contextual responses based on message analysis
        """
        
        # Build context from conversation history
        recent_context = " ".join([msg.get("content", "")[-100:] for msg in conversation_history[-3:]])
        message_lower = user_message.lower()
        
        # Enhanced response mapping based on scam indicators
        if any(word in message_lower for word in ['verify', 'confirm', 'update', 'reset']):
            responses = [
                "I'll verify my details right away. Which information do you need?",
                "Yes, I can confirm that information. What should I do next?",
                "I'm ready to update my account. Tell me exactly what to enter.",
                "I'll follow your instructions step by step.",
            ]
        elif any(word in message_lower for word in ['password', 'pin', 'otp', 'cvv']):
            responses = [
                "I have my password ready. Where should I provide it?",
                "My OTP is available. What's the process?",
                "I can share my PIN. Is it secure?",
                "Just give me instructions and I'll provide it.",
            ]
        elif any(word in message_lower for word in ['bank', 'account', 'transfer', 'send']):
            responses = [
                "I can transfer money. Where should I send it?",
                "My bank account is ready. What's the account number?",
                "How much money do you need me to send?",
                "I'll transfer immediately. Please provide the details.",
            ]
        elif any(word in message_lower for word in ['click', 'link', 'website', 'url']):
            responses = [
                "I'll click on that link now. What happens next?",
                "The page has loaded. What information should I enter?",
                "I've visited the website. What do I do now?",
                "I can see the login page. How do I proceed?",
            ]
        elif any(word in message_lower for word in ['money', 'rupees', 'amount', 'fee']):
            responses = [
                "How much money do I need to send?",
                "I can pay that amount. Where should I transfer it?",
                "What's the total cost?",
                "I'm ready to make the payment. Tell me the amount.",
            ]
        elif any(word in message_lower for word in ['urgent', 'immediately', 'hurry', 'asap']):
            responses = [
                "I'll do it right away! What should I do?",
                "I'm acting immediately. Give me the instructions.",
                "This sounds important. Tell me what to do.",
                "I'm in a hurry. Please give me quick instructions.",
            ]
        else:
            # Default responses based on conversation stage
            if len(conversation_history) < 2:
                responses = [
                    "I understand. What should I do next?",
                    "I can help with that. Please continue.",
                    "Yes, I'm listening. What else?",
                    "Go ahead, I'm ready to help.",
                ]
            else:
                responses = [
                    "I've done that. What's the next step?",
                    "Okay, I've completed that. What now?",
                    "Done. What should I do next?",
                    "I'm following along. Continue please.",
                ]
        
        # Pick a response based on conversation length for variety
        return responses[len(conversation_history) % len(responses)]
    
    def get_conversation_state(self, conversation_id: str) -> Optional[ConversationState]:
        """Retrieve conversation state"""
        return self.conversation_states.get(conversation_id)
    
    def terminate_conversation(self, conversation_id: str) -> bool:
        """Terminate a conversation"""
        if conversation_id in self.conversation_states:
            del self.conversation_states[conversation_id]
            return True
        return False
