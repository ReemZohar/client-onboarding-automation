# Client Onboarding Automation

Multi-agent pipeline for onboarding **Dapei Zahav** clients. Extracts data from websites, processes via LLM, generates personalized onboarding messages (for the client) and client info cards (for internal company usage).

## What It Does

Based on client URLs (their business website or minisite), the pipeline:
1. **Scrapes** all available text content from the URLs
2. **Extracts** structured data: business name, phone, email, address, services
3. **Generates** a personalized, warm onboarding message in Hebrew for the client
4. **Creates** a client card with all relevant information for internal company use

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
Navigates client websites and fetches all available text content. Tries requests/BeautifulSoup first, falls back to AI if blocked.

### Data Intelligence Agent
Takes raw scraped content and extracts structured fields: business name, phone, email, address, and services list. Returns clean data ready for the next agent.

### Copywriter Agent
Generates:
- **Client Card**: Internal summary for Dapei Zahav team with all client details
- **Onboarding Message**: Personalized welcome message in Hebrew, customized with client name, location, and services

## Tech Stack

- **opencode CLI** - Coding assistant
- **Python** - 3.10+
- **requests** - HTTP library for web requests
- **beautifulsoup4** - HTML parsing and scraping
- **python-dotenv** - Environment variable management
- **google-genai** - Google Gemini API client

## Project Structure

- `src/Orchestrator.py` - Central coordinator that sequences agents
- `src/agents.py` - Agent prompts and configuration
- `src/ScraperAgent.py`, `DataIntelligenceAgent.py`, `CopywriterAgent.py` - Individual agents
- `src/ui.html` - Simple UI to view the last client
- `src/crm_clients.json` - Local CRM storage
- `src/demourls.txt` - Sample URLs for testing

## Development & Approach

This project was built with **opencode CLI** as a coding assistant. Prompt engineering was done with **Google Gemini**. I refined the prompts iteratively and fed them to opencode to implement the agent logic.

- **Modularity**: Single responsibility per agent
- **LLM-powered**: Uses Google Gemini API for extraction and generation
- **Iterative refinement**: Focused on prompt engineering to get clean, personalized output

## Usage

### Prerequisites
- Python 3.10+

### Dependencies

```bash
pip install -r requirements.txt
```

### Setup
1. Copy `.env.example` to `.env`
2. Add your Gemini API key: `GEMINI_API_KEY=your_key_here`

### Run (WSL/Linux)
1. Pick your own URLs or use those from `src/demourls.txt`
2. Run: `python3 src/run.py <url1> <url2>`
   Example: `python3 src/run.py https://www.skai-kerur.co.il/ https://www.d.co.il/65462530/26250/`
3. Serve src folder: `cd src && python3 -m http.server 8000`
4. Open `http://localhost:8000/ui.html`