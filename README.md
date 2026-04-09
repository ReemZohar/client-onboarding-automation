# Client Onboarding Automation

Multi-agent pipeline for onboarding clients. Extracts data from websites, processes via LLM, and generates client artifacts.

## Development

This project was built with **opencode CLI** as a coding assistant.

## Libraries

- **requests** - HTTP library for web requests
- **beautifulsoup4** - HTML parsing and scraping
- **python-dotenv** - Environment variable management
- **google-genai** - Google Gemini API client

## Architecture

```
User Input → Pipeline (Orchestrator)
                ↓
Website/Minisite → Scraper Agent → Raw Content → Data Intelligence Agent → Structured Data
                                                                             ↓
                                                          Copywriter Agent → Client Card + Onboarding Message
                                                                             ↓
                                                             CRM (JSON file)
```

## Agents

### Scraper Agent
Navigates client websites and fetches all available text content. Uses requests and BeautifulSoup to extract raw HTML, or AI if extraction can't be made, then passes it forward.

### Data Intelligence Agent
Takes raw scraped content and extracts structured fields: business name, phone, email, address, and services list, using Gemini's API. Returns clean data ready for the next agent.

### Copywriter Agent
Generates the following from the structured data:
- **Client Card**: Internal summary for the Zap production team with all client details
- **Onboarding Message**: Personalized welcome message from Zap to the client in Hebrew, customized with their name, location, and services

## Files

- `src/Orchestrator.py` - Central coordinator that sequences agents
- `src/agents.py` - Agent prompts and configuration
- `src/ScraperAgent.py`, `DataIntelligenceAgent.py`, `CopywriterAgent.py` - Individual agents
- `src/ui.html` - Simple UI to view the last client
- `src/crm_clients.json` - Local CRM storage

## Approach

- **Modularity**: Single responsibility per agent
- **Local-first**: No external DB, just JSON file storage
- **LLM-powered**: Uses Google Gemini API for extraction and generation
- **Iterative refinement**: Focused on prompt engineering to get clean, personalized output

## Usage

### Dependencies

```bash
pip install -r requirements.txt
```

## Setup
1. Copy `.env.example` to `.env`
2. Add your Gemini API key: `GEMINI_API_KEY=your_key_here`

### Run (WSL/Linux)
1. Pick your own URLs or use those from `src/demourls.txt`
2. Run: `python3 src/run.py <ur1> <url2>`
   Example: `python3 src/run.py https://www.skai-kerur.co.il/ https://www.d.co.il/65462530/26250/`
3. Serve src folder: `cd src && python3 -m http.server 8000`
4. Open `http://localhost:8000/ui.html`