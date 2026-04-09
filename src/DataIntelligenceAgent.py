"""
Data Intelligence Agent
- Role: Parse raw text, identify entities
- Tools: Google Gemini API
- Inputs: Raw content from Scraper
- Outputs: Extracted entities (contact info, services/categories)
"""
import os
from dotenv import load_dotenv
from google import genai

from agents import get_agent_prompt

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class DataIntelligenceAgent:
    """Data Intelligence Agent - extracts structured entities from raw text."""
    
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.system_prompt = get_agent_prompt("data_intelligence")
    
    def _parse_response(self, text: str) -> dict:
        """Parse plain text response into client fields."""
        result = {
            "name": "",
            "phone": "",
            "email": "",
            "address": "",
            "services": [],
        }
        
        # Parse each line looking for field names
        for line in text.split("\n"):
            line = line.strip()
            
            # Check for single-value fields: name, phone, email, address
            for field in ["name", "phone", "email", "address"]:
                if line.startswith(f"{field}:"):
                    value = line.replace(f"{field}:", "").strip()
                    # Only set if value isn't "not found"
                    if value.lower() != "not found":
                        result[field] = value
                    break  # Move to next line
            
            # Check for services list (comma-separated)
            if line.startswith("services:"):
                value = line.replace("services:", "").strip()
                if value.lower() != "not found":
                    # Split by comma and clean each service name
                    result["services"] = [s.strip() for s in value.split(",") if s.strip()]
        
        return result
    
    def extract(self, raw_text: str) -> dict:
        """Extract structured entities from raw text and return a dict representing the client"""
        
        prompt = f"""{self.system_prompt}

Text to analyze:
{raw_text}"""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )
            
            return self._parse_response(response.text)
            
        except Exception as e:
            return {"error": str(e)}


def get_agent():
    """Factory function to get DataIntelligenceAgent instance."""
    return DataIntelligenceAgent()