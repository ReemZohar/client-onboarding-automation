"""
Orchestrator Agent
- Role: Central coordinator - sequences agents, manages workflow
- CRM: Local JSON file storage
"""
import json
import os
import time
from dotenv import load_dotenv

from ScraperAgent import get_agent as get_scraper
from DataIntelligenceAgent import get_agent as get_data_intel
from CopywriterAgent import get_agent as get_copywriter

load_dotenv()

CRM_FILE = "crm_clients.json"

class Orchestrator:
    def __init__(self):
        self.scraper = get_scraper()
        self.data_intel = get_data_intel()
        self.copywriter = get_copywriter()
    
    def run(self, urls: list[str]) -> dict:
        if not urls:
            return {"error": "No URLs provided"}
        
        print(f"[*] Processing {len(urls)} URL(s)")
        
        raw_data = self.scraper.scrape(urls)
        time.sleep(2)
        
        combined_text = "\n\n---\n\n".join(raw_data.values())
        
        print("[1/4] Extracting data...")
        structured = self.data_intel.extract(combined_text)
        time.sleep(2)
        
        if "error" in structured:
            return {"error": f"Extraction failed: {structured['error']}"}
        
        print("[2/4] Generating client card and personalized welcome message...")
        artifacts = self.copywriter.generate(structured)
        time.sleep(2)
        
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
        try:
            with open(CRM_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_client(self, client: dict):
        clients = self._load_clients()
        clients.append(client)
        with open(CRM_FILE, "w", encoding="utf-8") as f:
            json.dump(clients, f, ensure_ascii=False, indent=2)
        print(f"    -> Client saved")
    
    def get_clients(self) -> list:
        return self._load_clients()


def get_orchestrator():
    return Orchestrator()
