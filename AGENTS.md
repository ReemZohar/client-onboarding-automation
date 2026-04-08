# AGENTS.md

## System Overview

Multi-agent automation pipeline for onboarding home services clients, specifically an Air Conditioning Technician. Extracts data from websites, processes via LLM, generates a client object based on the data, syncs to CRM.

## Workflow

```
User Input → Pipeline (Orchestrator)
                ↓
Website/Minisite → Scraper Agent → Raw Content → Data Intelligence Agent → Structured Data
                                                                             ↓
                                                          Copywriter Agent → Client Card + Onboarding Message
                                                                             ↓
                                                             CRM (JSON file)
```

## Agent Catalog

### 1. Scraper/Extractor Agent
- **Role**: Navigate digital assets, retrieve raw content
- **Tools**: requests, BeautifulSoup, Google Gemini API
- **Inputs**: URLs
- **Outputs**: text content

### 2. Data Intelligence Agent
- **Role**: Parse raw text, identify entities
- **Tools**: Google Gemini API
- **Inputs**: Raw content from Scraper
- **Outputs**: Extracted entities (contact info, services/categories)

### 3. Copywriter Agent
- **Role**: Craft business artifacts
- **Tools**: Google Gemini API
- **Inputs**: Structured data from Data Intelligence Agent
- **Outputs**: Client Card (internal), Onboarding Message (client-facing)

## Data Schema

**Client Object** (stored in JSON):
- `name`: Client business name
- `phone`: Contact phone
- `email`: Contact email
- `address`: Physical address
- `services`: Comma-separated service categories
- `onboarding_msg`: Generated onboarding script (text)
- `client_card`: Generated client summary (text)

**Minimal Storage**: Local JSON file. No external DB required.

## Technical Principles

- **KISS**: Simple logic over complex abstractions
- **Modularity**: Single responsibility per agent
- **Scalability**: Easy to add new sources/outputs
- **Robustness**: Include error handling and data validation

## Agent Guidelines

- Only change code when explicitly asked
- Keep modifications minimal and focused on the specific task
- May add validation/error handling only in the specific part being worked on, not in unrelated parts of the file

## Commands
