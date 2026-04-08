"""
Copywriter Agent
- Role: Craft business artifacts (Client Card, Onboarding Script)
- Tools: Google Gemini API
- Inputs: Structured data from Data Intelligence Agent
- Outputs: Client Card text, Onboarding Script text
"""
import os
from dotenv import load_dotenv
from google import genai

from agents import get_agent_prompt

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class CopywriterAgent:
    """Copywriter Agent - generates business artifacts from client data."""
    
    def __init__(self):
        self.client = None
        if GEMINI_API_KEY:
            from google import genai
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.system_prompt = get_agent_prompt("copywriter")
    
    def generate_client_card(self, client_data: dict) -> str:
        """Generate internal Client Card for Zap production.
        
        Args:
            client_data: dict with name, phone, email, address, services
            
        Returns:
            Client Card text
        """
        prompt = f"""{self.system_prompt}

Generate a Client Card - an internal summary for Zap production team.

Client Information:
- Name: {client_data.get('name', 'N/A')}
- Phone: {client_data.get('phone', 'N/A')}
- Email: {client_data.get('email', 'N/A')}
- Address: {client_data.get('address', 'N/A')}
- Services Offered by the client: {', '.join(client_data.get('services', []))}

Create a structured Client Card with all relevant details formatted for internal use.
DO NOT include onboarding message - this is for internal team reference only."""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_onboarding_message(self, client_data: dict) -> str:
        """Generate personalized onboarding message from Zap.
        
        Args:
            client_data: dict with client information
            
        Returns:
            Onboarding message text
        """
        prompt = f"""{self.system_prompt}

Generate an onboarding message FROM ZAP to the client.

The message should:
- Welcome the client because they purchased a website from Zap
- Be warm and professional
- Mention the services they offer
- Be in Hebrew (since the client data is in Hebrew)
- Be short and friendly

Client Information:
- Business Name: {client_data.get('name', 'N/A')}
- Services Offered: {', '.join(client_data.get('services', []))}
- Phone: {client_data.get('phone', 'N/A')}"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate(self, client_data: dict) -> dict:
        """Generate both Client Card and Onboarding Message.
        
        Args:
            client_data: dict with client information
            
        Returns:
            dict with 'client_card' and 'onboarding_message'
        """
        return {
            "client_card": self.generate_client_card(client_data),
            "onboarding_message": self.generate_onboarding_message(client_data)
        }


def get_agent():
    """Factory function to get CopywriterAgent instance."""
    return CopywriterAgent()