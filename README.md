
# Contextual AI PPT Multi-Agent System

An intelligent **multi-agent AI system** that automatically generates **professional PowerPoint presentations**
from uploaded documents using **LangGraph**, **Retrieval-Augmented Generation (RAG)**, and **OpenAI LLMs**.

---

## Overview

This system accepts a topic, optional context, and reference documents (PDF, DOCX, TXT).
It retrieves relevant information using a vector database, coordinates multiple specialized agents,
and produces a polished `.pptx` file.

Design goals:
- Modularity
- Explainability
- Reusability
- Production readiness

---

## Features

### Multi-Agent Architecture
- Outline generation agent
- Content expansion agent
- Reviewer and quality control agent
- Export agent for PowerPoint generation

### Retrieval-Augmented Generation (RAG)
- Document ingestion and chunking
- FAISS-based semantic search
- Context-aware slide content with citations

### LangGraph Orchestration
- Explicit state management
- Deterministic execution flow
- Clean agent separation

### Interfaces
- Standalone Streamlit UI
- FastAPI backend (extensible)

---

## Architecture

User Topic + Context + Documents  
→ RAG Pipeline  
→ Outline Agent → Content Agent → Reviewer Agent → Export Agent  
→ Final `.pptx`

---

## Installation

```bash
git clone https://github.com/Kushagra3355/contextual_ai_ppt_multiagent_system.git
cd contextual_ai_ppt_multiagent_system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```env
OPENAI_API_KEY=sk-your-openai-api-key
```

---

## Usage

Run Streamlit app:
```bash
streamlit run streamlit_frontend.py
```

---

## Project Structure

Refer to the repository for a detailed modular folder layout including:
- agents
- rag_pipeline
- orchestrator
- tools
- schemas
- frontend and backend modules

---

## Technology Stack

- OpenAI, LangChain, LangGraph
- FAISS
- FastAPI
- Streamlit
- python-pptx
- Pydantic

---

## Roadmap

- Image generation for slides
- Template customization
- Multi-language support
- Cloud deployment guides
- Speaker notes generation

---

## Author

Kushagra Omar  
GitHub: https://github.com/Kushagra3355
