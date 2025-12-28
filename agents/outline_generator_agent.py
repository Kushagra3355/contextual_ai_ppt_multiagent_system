from langgraph.graph import StateGraph
from orchestrator.agent_state import Bulletslides, BulletslidesResponse
from app.dependencies import llm as get_llm
from rag_pipeline.pipeline import RAGPipeline


def OutlineAgent(state: dict) -> dict:
    """Generate presentation outline with titles and bullet points"""
    topic = state.get("topic", "")
    context = state.get("context", "")

    try:
        rag = RAGPipeline()
        rag.load()
        relevant_docs = rag.query(topic)
        rag_context = "\n\n".join([doc.page_content for doc in relevant_docs[:5]])
    except Exception as e:
        rag_context = "No relevant documents found."

    llm = get_llm()

    prompt = f"""
Create a presentation outline for the topic: {topic}

Context: {context}

Relevant Information from Knowledge Base:
{rag_context}

Based on the above information, generate 5-7 slides with clear titles and 3-4 bullet points each.
Focus on logical flow and key concepts from the retrieved data.

Return in this format:
Slide 1: [Title]
- [Bullet point 1]
- [Bullet point 2]
- [Bullet point 3]
"""

    response = llm.invoke(prompt)

    # Parse response into structured format
    slides = []
    lines = response.content.strip().split("\n")
    current_title = ""
    current_bullets = []

    for line in lines:
        line = line.strip()
        if line.startswith("Slide") and ":" in line:
            if current_title and current_bullets:
                slides.append(
                    Bulletslides(title=current_title, bullet_points=current_bullets)
                )
            current_title = line.split(":", 1)[1].strip()
            current_bullets = []
        elif line.startswith("-"):
            current_bullets.append(line[1:].strip())

    if current_title and current_bullets:
        slides.append(Bulletslides(title=current_title, bullet_points=current_bullets))

    result = BulletslidesResponse(slides=slides)
    return {"outline": result}
