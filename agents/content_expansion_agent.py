from orchestrator.agent_state import ExpandedContentResponse, PPTAgentState
from app.dependencies import llm as get_llm, get_rag_pipeline


def ContentExpansionAgent(state: PPTAgentState) -> PPTAgentState:
    """Expand bullet points into detailed content"""

    outline = state.outline
    topic = state.topic

    # Get RAG context once
    rag_context = ""
    try:
        rag = get_rag_pipeline()
        relevant_docs = rag.query(topic)
        rag_context = "\n\n".join([doc.page_content for doc in relevant_docs[:5]])
    except:
        pass

    # Use structured output
    llm = get_llm()
    structured_llm = llm.with_structured_output(ExpandedContentResponse)

    # Build slides text
    slides_text = "\n\n".join(
        [
            f"Slide: {slide.title}\nBullet Points:\n"
            + "\n".join(f"- {point}" for point in slide.bullet_points)
            for slide in outline.slides
        ]
    )

    prompt = f"""Expand each bullet point into 10-20 words factual sentences.

Topic: {topic}

{slides_text}

Knowledge Base Information:
{rag_context}

Keep content accurate and presentation-ready."""

    result = structured_llm.invoke(prompt)

    state.expanded_content = result.slides
    return state
