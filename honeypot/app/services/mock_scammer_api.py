import aiohttp
from typing import Dict, Optional
from app.config import Config


class MockScammerAPI:
    """Client to interact with Mock Scammer API for simulation"""
    
    def __init__(self, base_url: str = Config.MOCK_SCAMMER_API_URL, api_key: str = Config.MOCK_SCAMMER_API_KEY):
        self.base_url = base_url
        self.api_key = api_key
    
    async def send_message(self, conversation_id: str, message: str) -> Dict:
        """
        Send message to Mock Scammer API and get response
        
        Args:
            conversation_id: ID of the conversation
            message: Message to send to the mock scammer
            
        Returns:
            Response from mock scammer API
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {}
                if self.api_key:
                    headers['Authorization'] = f'Bearer {self.api_key}'
                
                payload = {
                    'conversation_id': conversation_id,
                    'message': message,
                }
                
                async with session.post(
                    f'{self.base_url}/scam/send',
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        return {
                            'error': f'API returned status {resp.status}',
                            'conversation_id': conversation_id
                        }
        except Exception as e:
            return {
                'error': str(e),
                'conversation_id': conversation_id
            }
    
    async def get_conversation(self, conversation_id: str) -> Dict:
        """Get conversation details from Mock Scammer API"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {}
                if self.api_key:
                    headers['Authorization'] = f'Bearer {self.api_key}'
                
                async with session.get(
                    f'{self.base_url}/scam/conversation/{conversation_id}',
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        return {
                            'error': f'API returned status {resp.status}',
                            'conversation_id': conversation_id
                        }
        except Exception as e:
            return {
                'error': str(e),
                'conversation_id': conversation_id
            }
    
    async def create_conversation(self, initial_message: str) -> Dict:
        """Create a new conversation with mock scammer"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {}
                if self.api_key:
                    headers['Authorization'] = f'Bearer {self.api_key}'
                
                payload = {'initial_message': initial_message}
                
                async with session.post(
                    f'{self.base_url}/scam/conversation',
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 201:
                        return await resp.json()
                    else:
                        return {
                            'error': f'API returned status {resp.status}'
                        }
        except Exception as e:
            return {
                'error': str(e)
            }
