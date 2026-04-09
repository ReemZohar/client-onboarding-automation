"""
Orchestrator Agent
- Role: Central coordinator - sequences agents, manages workflow
- CRM: Local JSON file storage
"""
import json
import time
from dotenv import load_dotenv

# Import agent factories
from ScraperAgent import get_agent as get_scraper
from DataIntelligenceAgent import get_agent as get_data_intel
from CopywriterAgent import get_agent as get_copywriter

load_dotenv()

# CRM storage file
CRM_FILE = "src/crm_clients.json"

class Orchestrator:
    """Central coordinator that sequences the agent pipeline."""
    
    def __init__(self):
        # Initialize all agents
        self.scraper = get_scraper()
        self.data_intel = get_data_intel()
        self.copywriter = get_copywriter()
    
    def run(self, urls: list[str]) -> dict:
        """Execute the full pipeline: scrape -> extract -> generate -> save."""
        
        if not urls:
            return {"error": "No URLs provided"}
        
        print(f"[*] Processing {len(urls)} URL(s)")
        
        # Step 1: Scrape raw content from URLs
        raw_data = self.scraper.scrape(urls)
        time.sleep(2)
        
        # Combine all scraped text into one string
        combined_text = "\n\n---\n\n".join(raw_data.values())
        
        # Step 2: Extract structured data from raw text
        print("[1/4] Extracting data...")
        structured = self.data_intel.extract(combined_text)
        time.sleep(2)
        
        if "error" in structured:
            return {"error": f"Extraction failed: {structured['error']}"}
        
        # Step 3: Generate client card and onboarding message
        print("[2/4] Generating client card and personalized welcome message...")
        artifacts = self.copywriter.generate(structured)
        time.sleep(2)
        
        # Step 4: Save to CRM
        print("[3/4] Saving to CRM...")
        client = {
            "name": structured.get("name", ""),
            "phone": structured.get("phone", ""),
            "email": structured.get("email", ""),
            "address": structured.get("address", ""),
            "services": structured.get("services", []),
            "client_card": artifacts.get("client_card", ""),
            "onboarding_msg": artifacts.get("onboarding_message", "")
        }
        self._save_client(client)
        
        return client
    
    def _load_clients(self) -> list:
        """Load all clients from CRM file."""
        try:
            with open(CRM_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_client(self, client: dict):
        """Append a new client to CRM file."""
        clients = self._load_clients()
        clients.append(client)
        with open(CRM_FILE, "w", encoding="utf-8") as f:
            json.dump(clients, f, ensure_ascii=False, indent=2)
        print(f"    -> Client saved")


def get_orchestrator():
    """Factory function to get Orchestrator instance."""
    return Orchestrator()
