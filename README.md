# Contextual AI PPT Multi-Agent System

Generate PowerPoint presentations from uploaded documents using a multi-agent AI pipeline.

## Setup

1. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables** – create a `.env` file in the project root with your API keys:
   ```
   OPENAI_API_KEY=sk-...
   ```

## Running the Application

### 1. Start the FastAPI backend

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`.

### 2. Start the Streamlit frontend

```bash
streamlit run frontend.py
```

Open the URL shown in your terminal (usually `http://localhost:8501`).

## Usage

1. Enter the **Topic** for your presentation.
2. Optionally add extra **Context**.
3. **Upload** one or more documents (PDF, TXT, DOCX, etc.).
4. Click **Generate PPT**.
5. Wait for processing (use _Check Status_ or enable _Auto-poll_).
6. Once complete, click **Download PPT**.

## Project Structure

```
contextual_ai_ppt_multiagent_system/
├── frontend.py                 # Streamlit UI for uploading docs & generating PPTs
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (OPENAI_API_KEY, etc.)
│
├── api/
│   └── main.py                 # FastAPI backend (endpoints: /generate-ppt, /task-status, /download)
│
├── app/
│   ├── config.py               # Application configuration settings
│   └── dependencies.py         # Dependency injection helpers
│
├── orchestrator/
│   ├── ppt_graph.py            # LangGraph workflow defining the multi-agent pipeline
│   └── agent_state.py          # Shared state schema passed between agents
│
├── agents/
│   ├── outline_generator_agent.py   # Generates slide outline from topic & context
│   ├── content_expansion_agent.py   # Expands bullet points with RAG-retrieved content
│   ├── format_optimizer_agent.py    # Optimizes slide layout & formatting
│   ├── reviewer_agent.py            # Reviews & refines generated content
│   └── export_agent.py              # Exports final state to .pptx file
│
├── rag_pipeline/
│   ├── pipeline.py             # High-level RAG orchestration (ingest + query)
│   ├── loader.py               # Document loaders (PDF, DOCX, TXT)
│   ├── splitter.py             # Text chunking strategies
│   ├── embedding.py            # Embedding model wrapper (OpenAI / local)
│   ├── vector_store.py         # FAISS vector store management
│   └── retriever.py            # Similarity search retriever
│
├── tools/
│   ├── chart_generator.py      # Generates charts for slides
│   ├── citation_tool.py        # Adds citations & references
│   ├── image_fetcher.py        # Fetches relevant images
│   └── web_search.py           # Web search for additional context
│
├── utils/
│   └── ppt_generator.py        # python-pptx helper to build .pptx files
│
├── schemas/
│   ├── ppt_schema.py           # Pydantic models for presentation structure
│   └── slide_schema.py         # Pydantic models for individual slides
│
├── data/
│   ├── documents/              # Sample/reference documents
│   └── uploads/                # User-uploaded files (per task_id)
│
├── vector_db/
│   └── index.faiss             # Persisted FAISS index
│
├── output/                     # Generated .pptx files
│
└── test/
    └── rag_test.py             # Unit tests for RAG pipeline
```

