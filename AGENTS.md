# AGENTS.md

## System Overview

Multi-agent automation pipeline for onboarding home services clients, specifically an Air Conditioning Technician. Extracts data from websites, processes via LLM, generates a client object based on the data, syncs to CRM.

## Workflow

```
User Input → Orchestrator Agent
                ↓
Website/Minisite → Scraper Agent → Raw Content → Data Intelligence Agent → Structured Data
                                                                            ↓
                                    CRM/Vector Store ← CRM Agent ← Client Card + Onboarding Script
```

## Agent Catalog

### 0. Orchestrator Agent
- **Role**: Central coordinator - receives input, decides which agent to invoke, manages flow
- **Tools**: LLM (routing logic), state management
- **Inputs**: User request (URLs to process)
- **Outputs**: Directed commands to specialist agents, final response to user
- **Logic**: Determines next step based on current pipeline state

### 1. Scraper/Extractor Agent
- **Role**: Navigate digital assets, retrieve raw content
- **Tools**: Google Gemini API
- **Inputs**: URLs (5-page website + minisite)
- **Outputs**: text content

### 2. Data Intelligence Agent
- **Role**: Parse raw text, identify entities
- **Tools**: Google Gemini API (free), regex, pydantic
- **Inputs**: Raw content from Scraper
- **Outputs**: Extracted entities (contact info, services/categories)

### 3. Copywriter Agent
- **Role**: Craft business artifacts
- **Tools**: Google Gemini API (free)
- **Inputs**: Structured data from Data Intelligence Agent
- **Outputs**: Client Card (internal), Onboarding Script (client-facing)

### 4. CRM/Integration Agent
- **Role**: Convert to Client objects, persist
- **Tools**: SQLite (built-in), json (for embedding vectors if needed later)
- **Inputs**: Structured data, generated artifacts
- **Outputs**: Persisted Client records in CRM

## Data Schema

**Client Object** (stored in SQLite):
- `id`: Unique identifier (auto-increment)
- `name`: Client business name
- `phone`: Contact phone
- `email`: Contact email
- `address`: Physical address
- `services`: Comma-separated service categories
- `onboarding_script`: Generated onboarding script (text)
- `client_card`: Generated client summary (text)

**Minimal Storage**: SQLite with 1 table (`clients`). No external DB required.

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
