from orchestrator.agent_state import ContentExpansion, BulletslidesResponse
from app.dependencies import llm as get_llm
from rag_pipeline.pipeline import RAGPipeline
from typing import List


def ContentExpansionAgent(state: dict) -> dict:
    """Expand bullet points into detailed content"""
    outline = state.get("outline")
    context = state.get("context", "")
    topic = state.get("topic", "")

    rag = RAGPipeline()
    try:
        rag.load()
        relevant_docs = rag.query(f"{topic} detailed information")
        rag_context = "\n\n".join([doc.page_content for doc in relevant_docs[:5]])
    except:
        rag_context = "No detailed information available."

    llm = get_llm()
    expanded_slides = []

    for slide in outline.slides:
        # Query RAG for slide-specific information
        try:
            slide_docs = rag.query(slide.title)
            slide_context = "\n".join([doc.page_content for doc in slide_docs[:3]])
        except:
            slide_context = ""

        prompt = f"""
Expand the following bullet points into detailed, factual statements:

Slide Title: {slide.title}
Bullet Points:
{chr(10).join(f"- {point}" for point in slide.bullet_points)}

Context: {context}

Relevant Knowledge Base Information:
{rag_context}

Slide-Specific Information:
{slide_context}

Provide 2-3 detailed, factual sentences for each bullet point using the retrieved information.
Keep content accurate and presentation-ready.
"""

        response = llm.invoke(prompt)
        detailed_points = [
            point.strip() for point in response.content.split("\n") if point.strip()
        ]

        expanded_slides.append(
            ContentExpansion(title=slide.title, detailed_points=detailed_points)
        )

    return {"expanded_content": expanded_slides}
