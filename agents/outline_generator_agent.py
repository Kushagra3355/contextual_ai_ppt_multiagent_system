from app.dependencies import llm as get_llm, get_rag_pipeline
from orchestrator.agent_state import BulletslidesResponse, PPTAgentState


def OutlineAgent(state: PPTAgentState) -> PPTAgentState:
    """Generates the outline"""

    topic = state.topic
    slides = state.slides

    rag_content = "No relevant documents found."
    try:
        rag = get_rag_pipeline()
        relevant_docs = rag.query(topic)
        if relevant_docs:
            rag_content = "\n\n".join([doc.page_content for doc in relevant_docs[:5]])
    except Exception:
        pass

    # Use structured output with BulletslidesResponse
    llm = get_llm()
    structured_llm = llm.with_structured_output(BulletslidesResponse)

    prompt = f"""You are an experienced outline designer.

Generate a concise, structured outline of EXACTLY {slides} slides about: {topic}

Knowledge Base Information:
{rag_content}

Create {slides} slides with:
- A clear, descriptive title for each slide
- 3-4 bullet points per slide
- Logical flow and key concepts from the knowledge base

If content is insufficient, distribute available information evenly across all {slides} slides."""

    # This returns a BulletslidesResponse object automatically
    result = structured_llm.invoke(prompt)

    # Update state with outline
    state.outline = result
    return state
