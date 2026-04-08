"""
Data Intelligence Agent
- Role: Parse raw text, identify entities
- Tools: Google Gemini API
- Inputs: Raw content from Scraper
- Outputs: Extracted entities (contact info, services/categories)
"""
import os
import re
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
        
        for line in text.split("\n"):
            line = line.strip()
            for field in ["name", "phone", "email", "address"]:
                if line.startswith(f"{field}:"):
                    value = line.replace(f"{field}:", "").strip()
                    if value.lower() != "not found":
                        result[field] = value
                    break
            
            if line.startswith("services:"):
                value = line.replace("services:", "").strip()
                if value.lower() != "not found":
                    result["services"] = [s.strip() for s in value.split(",") if s.strip()]
        
        return result
    
    def extract(self, raw_text: str) -> dict:
        """Extract structured entities from raw text.
        
        Args:
            raw_text: Raw text from Scraper Agent
            source_url: URL where the text came from
            
        Returns:
            dict with extracted client fields: name, phone, email, address, services
        """
        
        prompt = f"""{self.system_prompt}

Text to analyze:
{raw_text}"""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            return self._parse_response(response.text)
            
        except Exception as e:
            return {"error": str(e)}
    
    def extract_batch(self, raw_data: dict) -> dict:
        """Extract from multiple URLs and merge into single client entity."""
        merged = {
            "name": "",
            "phone": "",
            "email": "",
            "address": "",
            "services": [],
        }
        
        single_fields = ["name", "phone", "email", "address"]
        
        for text in raw_data.items():
            result = self.extract(text)
            
            if "error" in result:
                continue
            
            # Merges the fields that have a single value into one entity
            for field in single_fields:
                if not merged[field] and result.get(field):
                    merged[field] = result[field]
            
            # Merges the services extracted from each source into a single list
            for service in result.get("services", []):
                if service and service not in merged["services"]:
                    merged["services"].append(service)
        
        return merged


def get_agent():
    """Factory function to get DataIntelligenceAgent instance."""
    return DataIntelligenceAgent()