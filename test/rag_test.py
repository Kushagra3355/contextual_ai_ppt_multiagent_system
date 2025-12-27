import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag_pipeline.pipeline import RAGPipeline
from app.dependencies import llm as llm_factory


# -----------------------------
# 1. Initialize pipeline
# -----------------------------
rag = RAGPipeline()

# Run ONCE when documents change
# rag.ingest("data/documents")

# Normal usage
rag.load()


# -----------------------------
# 2. Query
# -----------------------------
query = "define current"

docs = rag.query(query)


# -----------------------------
# 3. Build context WITH citations
# -----------------------------
context_parts = []

for i, d in enumerate(docs, start=1):
    source = d.metadata.get("filename", "unknown")
    page = d.metadata.get("page", "N/A")

    context_parts.append(
        f"[{i}] Source: {source}, Page: {page}\n{d.page_content}"
    )

context = "\n\n".join(context_parts)


# -----------------------------
# 4. LLM Call
# -----------------------------
llm = llm_factory()

response = llm.invoke(
    f"""Answer strictly using the context below.
If not found, say "Not found".
Cite sources using file name and page number of the document.

Context:
{context}

Question:
{query}
"""
)

print(response.content)
