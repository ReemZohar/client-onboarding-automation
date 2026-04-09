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
        # Initialize Gemini client for AI fallback
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.system_prompt = get_agent_prompt("scraper")
    
    def fetch_with_ai(self, url: str) -> str:
        """Fallback: use AI to fetch URL content when scraping fails."""
        
        try:
            # Ask Gemini to extract the page content
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
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
                # Try HTTP request first
                response = requests.get(url, timeout=15)
                
                # If blocked (403), fall back to AI
                if response.status_code == 403:
                    results[url] = self.fetch_with_ai(url)
                else:
                    # Parse HTML and extract visible text
                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    # Remove noisy elements (scripts, styles, nav, footer)
                    for tag in soup(['script', 'style', 'nav', 'footer']):
                        tag.decompose()
                    
                    results[url] = soup.get_text()
                    
            except Exception:
                # On any error, try AI fallback
                results[url] = self.fetch_with_ai(url)
        
        return results

def get_agent():
    """Factory function to get ScraperAgent instance."""
    return ScraperAgent()