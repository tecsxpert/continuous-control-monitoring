# Continuous Control Monitoring

# AI Service — CampusPe CCM Project

## Overview

This AI service provides intelligent analysis of security and compliance issues using Large Language Models (LLMs). It supports risk description, recommendations, report generation, document analysis, batch processing, and real-time streaming.

---

## Features

- Generate professional risk descriptions
- Provide actionable recommendations
- Generate structured audit reports
- Analyze documents for risks and insights
- Batch processing with rate control
- Real-time streaming using SSE
- RAG (Retrieval-Augmented Generation) for context-aware responses
- Unit tested with pytest (mocked AI responses)

---

## Tech Stack

- Python (Flask)
- Groq LLM API
- ChromaDB (RAG)
- Sentence Transformers
- Pytest (testing)

---

## Project Structure

ai-service/
│
├── routes/ # API endpoints
├── services/ # AI logic, RAG, Groq client
├── prompts/ # Prompt templates
├── tests/ # Unit tests
├── app.py # Entry point
├── run_rag.py # RAG pipeline setup
└── requirements.txt

---

## Prerequisites

- Python 3.10+
- pip
- Groq API key

---

## Setup Instructions

```bash
git clone <repo-url>

cd ai-service

pip install -r requirements.txt
```

## Environment Variables

Create a .env file in the root:
GROQ_API_KEY=your_api_key_here

## Run the Service

python app.py

Service will run on
http://127.0.0.1:5000

## API Endpoints

#Health Check
Get /health

#Describe Issue
POST /describe

Request
{
"title": "...",
"description": "..."
}

#Recommendations
POST /recommend

#Generate Report
POST /generate-report

#Stream Report(SSE)
GET /generate-report/stream?title=...&description=...

#Analyse Document
POST /analyse-document

Request
{
"text": "..."
}

#Batch Processing
POST /batch-process
{
"items": [
{"title": "...", "description": "..."}
]
}

## Running Tests

python -m pytest -v
