#  Contextual AI PPT Multi-Agent System

An intelligent, multi-agent AI system that automatically generates professional PowerPoint presentations from uploaded documents using **LangGraph**, **RAG (Retrieval-Augmented Generation)**, and **OpenAI**.

##  Features

- ** Multi-Agent Architecture**: Orchestrated workflow with specialized agents for outline generation, content expansion, review, and export
- ** RAG Pipeline**: Retrieves relevant context from uploaded documents (PDF, DOCX, TXT) using FAISS vector store
- ** LangGraph Workflow**: Structured agent orchestration with state management
- ** Streamlit UI**: Interactive web interface for easy presentation generation
- ** FastAPI Backend**: RESTful API for asynchronous task processing
- ** Smart Content**: AI-powered content expansion with citations and contextual information
- ** Multi-Format Support**: Upload and process various document formats
- ** Persistent Storage**: Vector database persistence for efficient retrieval

##  Architecture

The system uses a **multi-agent workflow** powered by LangGraph:

1. **Outline Generator Agent**: Creates initial slide structure based on topic and context
2. **Content Expansion Agent**: Enriches slides with relevant information from RAG pipeline
3. **Reviewer Agent**: Validates and refines content quality
4. **Export Agent**: Generates final PowerPoint file

```
Topic + Context + Documents
          ↓
    [RAG Pipeline]
          ↓
   Outline Agent → Content Expansion → Reviewer → Export
          ↓              ↓               ↓           ↓
      Slides        Enhanced Text    Quality QA   .pptx
```

##  Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- pip package manager

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Kushagra3355/contextual_ai_ppt_multiagent_system.git
   cd contextual_ai_ppt_multiagent_system
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ```

##  Usage

### Option 1: Standalone Streamlit App (Recommended for Quick Start)

```bash
streamlit run streamlit_frontend.py
```

Access the app at `http://localhost:8501`

### Option 2: FastAPI Backend + Frontend 

(coming soon!!)

###  Generating Presentations

1. **Enter Topic**: Specify the presentation subject
2. **Add Context** (optional): Provide additional details or requirements
3. **Upload Documents**: Select PDF, DOCX, or TXT files for context
4. **Configure Settings**:
   - Number of slides
   - Content depth
   - Style preferences
5. **Generate**: Click "Generate PPT" and wait for processing
6. **Download**: Retrieve your generated PowerPoint presentation

##  Project Structure

```
contextual_ai_ppt_multiagent_system/
├──  frontend.py                        # Streamlit UI (API-based)
├──  streamlit_frontend.py              # Standalone Streamlit app
├──  requirements.txt                   # Python dependencies
├──  .env                               # Environment variables (OPENAI_API_KEY)
│
├──  api/
│   └── main.py                          # FastAPI backend with endpoints
│
├──  app/
│   ├── config.py                        # Application configuration
│   └── dependencies.py                  # Dependency injection
│
├──  orchestrator/
│   ├── ppt_graph.py                     # LangGraph workflow definition
│   └── agent_state.py                   # Shared state schema between agents
│
├──  agents/
│   ├── outline_generator_agent.py       # Creates slide structure
│   ├── content_expansion_agent.py       # Expands content with RAG
│   ├── reviewer_agent.py                # Reviews and refines content
│   └── export_agent.py                  # Generates .pptx file
│
├──  rag_pipeline/
│   ├── pipeline.py                      # RAG orchestration
│   ├── loader.py                        # Document loaders (PDF, DOCX, TXT)
│   ├── splitter.py                      # Text chunking strategies
│   ├── embedding.py                     # Embedding model (OpenAI)
│   ├── vector_store.py                  # FAISS vector store management
│   └── retriever.py                     # Similarity search retriever
│
├──  tools/
│   ├── chart_generator.py               # Chart generation for slides
│   ├── citation_tool.py                 # Citation management
│   ├── image_fetcher.py                 # Image retrieval
│   └── web_search.py                    # Web search integration
│
├──  utils/
│   └── ppt_generator.py                 # python-pptx helper functions
│
├──  schemas/
│   ├── ppt_schema.py                    # Presentation data models
│   └── slide_schema.py                  # Slide data models
│
├──  data/
│   ├── documents/                       # Reference documents
│   ├── uploads/                         # User uploads (by task_id)
│   └── draft.txt                        # Draft content
│
├──  vector_db/
│   └── index.faiss                      # Persisted FAISS index
│
├──  output/                           # Generated .pptx files
│
└──  test/
    ├── agent_test.py                    # Agent unit tests
    └── rag_test.py                      # RAG pipeline tests
```

##  Technology Stack

| Category                | Technologies                     |
| ----------------------- | -------------------------------- |
| **AI/ML**               | OpenAI GPT, LangChain, LangGraph |
| **Vector DB**           | FAISS                            |
| **Backend**             | FastAPI, Python 3.8+             |
| **Frontend**            | Streamlit                        |
| **Document Processing** | PyPDF, python-docx, docx2txt     |
| **Presentation**        | python-pptx                      |
| **Data Models**         | Pydantic                         |


##  Customization

### Modifying Agents

Each agent is modular and can be customized:

- **Outline Agent**: Adjust slide structure and titles
- **Content Expansion**: Modify RAG retrieval parameters
- **Reviewer**: Change validation criteria
- **Export**: Customize PowerPoint styling

### RAG Pipeline Configuration

Configure in [rag_pipeline/pipeline.py](rag_pipeline/pipeline.py):

- Chunk size and overlap
- Embedding model
- Retrieval parameters (top_k, similarity threshold)


##  Acknowledgments

- **LangChain** for the LLM framework
- **LangGraph** for agent orchestration
- **OpenAI** for language models
- **FAISS** for efficient vector search
- **Streamlit** for rapid UI development

##  Contact

**Kushagra** - [@Kushagra3355](https://github.com/Kushagra3355)

Project Link: [https://github.com/Kushagra3355/contextual_ai_ppt_multiagent_system](https://github.com/Kushagra3355/contextual_ai_ppt_multiagent_system)

##  Roadmap

- [ ] Add support for more document formats (Markdown, HTML)
- [ ] Implement image generation for slides
- [ ] Add template customization options
- [ ] Multi-language support
- [ ] Real-time collaboration features
- [ ] Cloud deployment guide (AWS, Azure, GCP)
- [ ] Enhanced chart and data visualization
- [ ] Speaker notes generation

---


