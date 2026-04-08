"""
Scraper/Extractor Agent
- Role: Navigate digital assets, retrieve raw content
- Tools: Google Gemini API
- Inputs: URLs
- Outputs: text content
"""
import os
from dotenv import load_dotenv

from agents import get_agent_prompt

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class ScraperAgent:
    """Scraper/Extractor Agent - retrieves raw content from URLs using AI."""
    
    def __init__(self):
        self.client = None
        if GEMINI_API_KEY:
            from google import genai
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.system_prompt = get_agent_prompt("scraper")
    
    def fetch(self, url: str) -> str:
        """Use AI to fetch all content from URL."""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=self.system_prompt + f"\n\nURL to fetch: {url}"
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def scrape(self, urls: list[str]) -> dict:
        """Scrape URLs using AI."""
        results = {}
        for url in urls:
            results[url] = self.fetch(url)
        return results

def get_agent():
    """Factory function to get ScraperAgent instance."""
    return ScraperAgent()

if __name__ == "__main__":
    with open("src/demourls.txt") as f:
        urls = [u.strip() for u in f if u.strip()]
    
    agent = ScraperAgent()
    output = agent.scrape(urls)