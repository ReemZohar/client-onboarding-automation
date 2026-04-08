"""
Scraper/Extractor Agent
- Role: Navigate digital assets, retrieve raw content
- Tools: requests, BeautifulSoup, Google Gemini API
- Inputs: URLs
- Outputs: text content
"""
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from google import genai

from agents import get_agent_prompt

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class ScraperAgent:
    """Scraper/Extractor Agent - retrieves raw content from URLs."""
    
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.system_prompt = get_agent_prompt("scraper")
    
    def fetch_with_ai(self, url: str) -> str:
        """Fallback: use AI to fetch URL content when scraping fails."""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{self.system_prompt}\n\nURL to fetch: {url}"
            )
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def scrape(self, urls: list[str]) -> dict:
        """Scrape URLs with AI fallback on failure."""
        results = {}
        for url in urls:
            try:
                response = requests.get(url, timeout=15)
                if response.status_code == 403:
                    results[url] = self.fetch_with_ai(url)
                else:
                    soup = BeautifulSoup(response.text, "html.parser")
                    for tag in soup(['script', 'style', 'nav', 'footer']):
                        tag.decompose()
                    results[url] = soup.get_text()
            except Exception as e:
                results[url] = self.fetch_with_ai(url)
        return results

def get_agent():
    """Factory function to get ScraperAgent instance."""
    return ScraperAgent()